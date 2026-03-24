from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator
import uuid


class CustomUser(AbstractUser):
    """
    Custom user model extending Django's AbstractUser.
    This model will be used throughout the RetailShop API.
    """
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    is_customer = models.BooleanField(default=True)
    is_staff_member = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username

    class Meta:
        db_table = 'custom_user'
        verbose_name = 'User'
        verbose_name_plural = 'Users'


class Registration(models.Model):
    """
    Registration model to track user registration process.
    """
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    ]
    
    REGISTRATION_TYPE_CHOICES = [
        ('customer', 'Customer'),
        ('staff', 'Staff Member'),
        ('admin', 'Admin'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='registration')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    registration_type = models.CharField(max_length=20, choices=REGISTRATION_TYPE_CHOICES, default='customer')
    confirmation_token = models.CharField(max_length=100, unique=True, blank=True)
    is_email_verified = models.BooleanField(default=False)
    registration_date = models.DateTimeField(auto_now_add=True)
    confirmed_date = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.status}"
    
    class Meta:
        db_table = 'registration'
        verbose_name = 'Registration'
        verbose_name_plural = 'Registrations'


class EmailVerification(models.Model):
    """
    Model to track email verification tokens.
    """
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='email_verifications')
    token = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Email verification for {self.user.username}"
    
    class Meta:
        db_table = 'email_verification'
        verbose_name = 'Email Verification'
        verbose_name_plural = 'Email Verifications'


class PasswordReset(models.Model):
    """
    Model to track password reset tokens.
    """
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='password_resets')
    token = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Password reset for {self.user.username}"
    
    class Meta:
        db_table = 'password_reset'
        verbose_name = 'Password Reset'
        verbose_name_plural = 'Password Resets'


class UserProfile(models.Model):
    """
    Extended user profile with additional information.
    """
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
        ('P', 'Prefer not to say'),
    ]
    
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)
    bio = models.TextField(max_length=500, blank=True)
    website = models.URLField(blank=True)
    social_media_links = models.JSONField(default=dict, blank=True)
    preferences = models.JSONField(default=dict, blank=True)
    notification_settings = models.JSONField(default=dict, blank=True)
    last_login_ip = models.GenericIPAddressField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username}'s Profile"
    
    class Meta:
        db_table = 'user_profile'
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'
