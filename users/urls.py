from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CustomUserViewSet
from .registration_views import (
    RegisterView, VerifyEmailView, LoginView, LogoutView, RefreshTokenView,
    PasswordResetRequestView, PasswordResetConfirmView, UserProfileView, 
    RegistrationListView, RegistrationStatusView
)

router = DefaultRouter()
router.register(r'users', CustomUserViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    
    # Registration endpoints
    path('api/auth/register/', RegisterView.as_view(), name='register'),
    path('api/auth/verify-email/<str:token>/', VerifyEmailView.as_view(), name='verify-email'),
    path('api/auth/login/', LoginView.as_view(), name='login'),
    path('api/auth/logout/', LogoutView.as_view(), name='logout'),
    path('api/auth/refresh/', RefreshTokenView.as_view(), name='token-refresh'),
    path('api/auth/password-reset/', PasswordResetRequestView.as_view(), name='password-reset'),
    path('api/auth/password-reset-confirm/', PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
    path('api/auth/profile/', UserProfileView.as_view(), name='user-profile'),
    path('api/auth/registration-status/', RegistrationStatusView.as_view(), name='registration-status'),
    
    # Admin endpoints
    path('api/admin/registrations/', RegistrationListView.as_view(), name='registration-list'),
]
