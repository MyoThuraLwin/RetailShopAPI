from rest_framework import serializers
from django.contrib.auth.models import Group
from .models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    """
    Serializer for the CustomUser model.
    Handles serialization and validation of user data.
    """
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 
                  'phone_number', 'address', 'date_of_birth', 'is_customer',
                  'is_staff_member', 'is_active', 'date_joined', 'password']
        extra_kwargs = {
            'password': {'write_only': True},
            'date_joined': {'read_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = CustomUser(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        if password:
            instance.set_password(password)
        
        instance.save()
        return instance
