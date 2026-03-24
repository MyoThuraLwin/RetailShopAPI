from rest_framework import status, generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate, login
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from .models import CustomUser, Registration, EmailVerification, PasswordReset, UserProfile
from .registration_serializers import (
    RegistrationSerializer, EmailVerificationSerializer,
    PasswordResetSerializer, PasswordResetConfirmSerializer,
    UserProfileSerializer, RegistrationDetailSerializer
)


class RegisterView(APIView):
    """
    API endpoint for user registration.
    """
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            
            # Send verification email (in production, use proper email service)
            try:
                registration = Registration.objects.get(user=user)
                verification_url = f"{settings.FRONTEND_URL}/verify-email/{registration.confirmation_token}/"
                
                send_mail(
                    'Verify your email address',
                    f'Please click the following link to verify your email: {verification_url}',
                    settings.DEFAULT_FROM_EMAIL,
                    [user.email],
                    fail_silently=False,
                )
            except Exception as e:
                # Log error but don't fail registration
                pass
            
            return Response({
                'message': 'Registration successful. Please check your email for verification.',
                'user_id': user.id,
                'username': user.username
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyEmailView(APIView):
    """
    API endpoint for email verification.
    """
    permission_classes = [permissions.AllowAny]
    
    def get(self, request, token):
        try:
            registration = Registration.objects.get(confirmation_token=token)
            
            if registration.status == 'confirmed':
                return Response({
                    'message': 'Email already verified.'
                }, status=status.HTTP_200_OK)
            
            # Update registration status
            registration.status = 'confirmed'
            registration.is_email_verified = True
            registration.confirmed_date = timezone.now()
            registration.save()
            
            # Activate user account
            user = registration.user
            user.is_active = True
            user.save()
            
            return Response({
                'message': 'Email verified successfully. Your account is now active.'
            }, status=status.HTTP_200_OK)
            
        except Registration.DoesNotExist:
            return Response({
                'error': 'Invalid verification token.'
            }, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    """
    API endpoint for user login.
    """
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        
        if not username or not password:
            return Response({
                'error': 'Username and password are required.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        user = authenticate(username=username, password=password)
        
        if user is not None:
            if not user.is_active:
                return Response({
                    'error': 'Account is not active. Please verify your email.'
                }, status=status.HTTP_401_UNAUTHORIZED)
            
            # In production, generate JWT token here
            return Response({
                'message': 'Login successful.',
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'is_customer': user.is_customer,
                    'is_staff_member': user.is_staff_member
                }
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'error': 'Invalid credentials.'
            }, status=status.HTTP_401_UNAUTHORIZED)


class PasswordResetRequestView(APIView):
    """
    API endpoint for password reset request.
    """
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = PasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            password_reset = serializer.save()
            
            # Send password reset email
            try:
                reset_url = f"{settings.FRONTEND_URL}/reset-password/{password_reset.token}/"
                
                send_mail(
                    'Reset your password',
                    f'Please click the following link to reset your password: {reset_url}',
                    settings.DEFAULT_FROM_EMAIL,
                    [password_reset.user.email],
                    fail_silently=False,
                )
            except Exception as e:
                # Log error but don't fail the request
                pass
            
            return Response({
                'message': 'Password reset link sent to your email.'
            }, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetConfirmView(APIView):
    """
    API endpoint for password reset confirmation.
    """
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            
            return Response({
                'message': 'Password reset successful.'
            }, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(generics.RetrieveUpdateAPIView):
    """
    API endpoint for viewing and updating user profile.
    """
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        profile, created = UserProfile.objects.get_or_create(user=self.request.user)
        return profile


class RegistrationListView(generics.ListAPIView):
    """
    API endpoint for listing registrations (admin only).
    """
    queryset = Registration.objects.all()
    serializer_class = RegistrationDetailSerializer
    permission_classes = [permissions.IsAdminUser]


class RegistrationStatusView(APIView):
    """
    API endpoint for checking registration status.
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        try:
            registration = Registration.objects.get(user=request.user)
            serializer = RegistrationDetailSerializer(registration)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Registration.DoesNotExist:
            return Response({
                'error': 'Registration not found.'
            }, status=status.HTTP_404_NOT_FOUND)
