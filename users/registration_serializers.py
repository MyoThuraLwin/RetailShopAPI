from rest_framework import serializers
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import CustomUser, Registration, EmailVerification, PasswordReset, UserProfile
import uuid

from .serializers import CustomUserSerializer


class RegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration process.
    """
    password = serializers.CharField(write_only=True, min_length=8)
    confirm_password = serializers.CharField(write_only=True)
    
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name', 'password', 
                  'confirm_password', 'phone_number', 'address', 'date_of_birth']
    
    def validate_email(self, value):
        if CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value
    
    def validate_username(self, value):
        if CustomUser.objects.filter(username=value).exists():
            raise serializers.ValidationError("A user with this username already exists.")
        return value
    
    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords don't match.")
        return data
    
    def create(self, validated_data):
        validated_data.pop('confirm_password')
        password = validated_data.pop('password')
        
        user = CustomUser.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        
        # Create registration record
        registration = Registration.objects.create(
            user=user,
            confirmation_token=str(uuid.uuid4())
        )
        
        # Create user profile
        UserProfile.objects.create(user=user)
        
        return user


class EmailVerificationSerializer(serializers.ModelSerializer):
    """
    Serializer for email verification.
    """
    class Meta:
        model = EmailVerification
        fields = ['token', 'user', 'created_at', 'expires_at']
        read_only_fields = ['user', 'created_at', 'expires_at']


class PasswordResetSerializer(serializers.Serializer):
    """
    Serializer for password reset request.
    """
    email = serializers.EmailField()
    
    def validate_email(self, value):
        if not CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("No user found with this email address.")
        return value
    
    def create(self, validated_data):
        email = validated_data['email']
        user = CustomUser.objects.get(email=email)
        
        # Invalidate existing tokens
        PasswordReset.objects.filter(user=user, is_used=False).update(is_used=True)
        
        # Create new token
        token = str(uuid.uuid4())
        expires_at = timezone.now() + timezone.timedelta(hours=1)
        
        password_reset = PasswordReset.objects.create(
            user=user,
            token=token,
            expires_at=expires_at
        )
        
        return password_reset


class PasswordResetConfirmSerializer(serializers.Serializer):
    """
    Serializer for password reset confirmation.
    """
    token = serializers.CharField()
    new_password = serializers.CharField(min_length=8, write_only=True)
    confirm_password = serializers.CharField(write_only=True)
    
    def validate_token(self, value):
        try:
            reset = PasswordReset.objects.get(token=value, is_used=False)
            if reset.expires_at < timezone.now():
                raise serializers.ValidationError("Token has expired.")
            return value
        except PasswordReset.DoesNotExist:
            raise serializers.ValidationError("Invalid token.")
    
    def validate(self, data):
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords don't match.")
        return data
    
    def save(self):
        token = self.validated_data['token']
        new_password = self.validated_data['new_password']
        
        reset = PasswordReset.objects.get(token=token, is_used=False)
        user = reset.user
        
        user.set_password(new_password)
        user.save()
        
        reset.is_used = True
        reset.save()
        
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for user profile.
    """
    class Meta:
        model = UserProfile
        fields = ['profile_picture', 'gender', 'bio', 'website', 'social_media_links',
                  'preferences', 'notification_settings', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']


class RegistrationDetailSerializer(serializers.ModelSerializer):
    """
    Detailed serializer for registration with user information.
    """
    user = CustomUserSerializer(read_only=True)
    
    class Meta:
        model = Registration
        fields = ['id', 'user', 'registration_type', 'status', 'is_email_verified',
                  'is_phone_verified', 'registration_date', 'confirmed_date', 'notes']
        read_only_fields = ['id', 'registration_date', 'confirmed_date']
