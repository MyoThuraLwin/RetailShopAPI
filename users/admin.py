from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Registration, EmailVerification, PasswordReset, UserProfile


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """
    Admin configuration for CustomUser model.
    Extends Django's UserAdmin to include custom fields.
    """
    list_display = ['username', 'email', 'first_name', 'last_name', 'phone_number', 'is_customer', 'is_staff_member', 'is_active']
    list_filter = ['is_active', 'is_customer', 'is_staff_member', 'date_joined']
    search_fields = ['username', 'email', 'first_name', 'last_name', 'phone_number']
    
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Information', {
            'fields': ('phone_number', 'address', 'date_of_birth', 'is_customer', 'is_staff_member')
        }),
    )
    
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Additional Information', {
            'fields': ('email', 'phone_number', 'address', 'date_of_birth', 'is_customer', 'is_staff_member')
        }),
    )


@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    """
    Admin configuration for Registration model.
    """
    list_display = ['user', 'registration_type', 'status', 'is_email_verified', 'registration_date']
    list_filter = ['status', 'registration_type', 'is_email_verified', 'registration_date']
    search_fields = ['user__username', 'user__email']
    readonly_fields = ['id', 'registration_date', 'confirmed_date', 'confirmation_token']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('user', 'registration_type', 'status')
        }),
        ('Verification', {
            'fields': ('is_email_verified', 'confirmation_token')
        }),
        ('Timestamps', {
            'fields': ('registration_date', 'confirmed_date')
        }),
        ('Additional', {
            'fields': ('notes',)
        }),
    )


@admin.register(EmailVerification)
class EmailVerificationAdmin(admin.ModelAdmin):
    """
    Admin configuration for EmailVerification model.
    """
    list_display = ['user', 'token', 'created_at', 'expires_at', 'is_used']
    list_filter = ['is_used', 'created_at', 'expires_at']
    search_fields = ['user__username', 'user__email', 'token']
    readonly_fields = ['token', 'created_at', 'expires_at']


@admin.register(PasswordReset)
class PasswordResetAdmin(admin.ModelAdmin):
    """
    Admin configuration for PasswordReset model.
    """
    list_display = ['user', 'token', 'created_at', 'expires_at', 'is_used']
    list_filter = ['is_used', 'created_at', 'expires_at']
    search_fields = ['user__username', 'user__email', 'token']
    readonly_fields = ['token', 'created_at', 'expires_at']


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """
    Admin configuration for UserProfile model.
    """
    list_display = ['user', 'gender', 'website', 'created_at', 'updated_at']
    list_filter = ['gender', 'created_at']
    search_fields = ['user__username', 'user__email', 'bio']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('user', 'profile_picture', 'gender')
        }),
        ('Personal Details', {
            'fields': ('bio', 'website', 'social_media_links')
        }),
        ('Settings', {
            'fields': ('preferences', 'notification_settings')
        }),
        ('System Information', {
            'fields': ('last_login_ip', 'created_at', 'updated_at')
        }),
    )
