from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework.test import APITestCase
from rest_framework import status
from .models import CustomUser, Registration, EmailVerification, PasswordReset, UserProfile
from .registration_serializers import RegistrationSerializer, PasswordResetSerializer
import uuid


class CustomUserModelTests(TestCase):
    """
    Test cases for the CustomUser model.
    """

    def setUp(self):
        self.user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'first_name': 'Test',
            'last_name': 'User',
            'phone_number': '1234567890',
            'address': '123 Test Street',
            'is_customer': True,
            'is_staff_member': False,
        }

    def test_create_user(self):
        """
        Test creating a new user with all custom fields.
        """
        user = CustomUser.objects.create_user(**self.user_data)
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'test@example.com')
        self.assertEqual(user.phone_number, '1234567890')
        self.assertTrue(user.is_customer)
        self.assertFalse(user.is_staff_member)

    def test_user_str_representation(self):
        """
        Test the string representation of the user.
        """
        user = CustomUser.objects.create_user(**self.user_data)
        self.assertEqual(str(user), 'testuser')

    def test_custom_user_model_is_used(self):
        """
        Test that the custom user model is properly configured.
        """
        User = get_user_model()
        self.assertEqual(User.__name__, 'CustomUser')
        self.assertEqual(User._meta.db_table, 'custom_user')


class RegistrationModelTests(TestCase):
    """
    Test cases for the Registration model.
    """

    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

    def test_create_registration(self):
        """
        Test creating a registration record.
        """
        registration = Registration.objects.create(
            user=self.user,
            registration_type='customer',
            confirmation_token=str(uuid.uuid4())
        )
        self.assertEqual(registration.user, self.user)
        self.assertEqual(registration.status, 'pending')
        self.assertFalse(registration.is_email_verified)

    def test_registration_str_representation(self):
        """
        Test the string representation of registration.
        """
        registration = Registration.objects.create(
            user=self.user,
            confirmation_token=str(uuid.uuid4())
        )
        expected = f"{self.user.username} - {registration.status}"
        self.assertEqual(str(registration), expected)


class RegistrationAPITests(APITestCase):
    """
    Test cases for registration API endpoints.
    """

    def setUp(self):
        self.registration_data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'first_name': 'New',
            'last_name': 'User',
            'password': 'strongpass123',
            'confirm_password': 'strongpass123',
            'phone_number': '9876543210',
            'address': '456 New Street'
        }

    def test_registration_success(self):
        """
        Test successful user registration.
        """
        response = self.client.post('/api/auth/register/', self.registration_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('message', response.data)
        self.assertIn('user_id', response.data)

    def test_registration_password_mismatch(self):
        """
        Test registration with mismatched passwords.
        """
        data = self.registration_data.copy()
        data['confirm_password'] = 'differentpass'
        response = self.client.post('/api/auth/register/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_registration_duplicate_email(self):
        """
        Test registration with duplicate email.
        """
        CustomUser.objects.create_user(
            username='existing',
            email='existing@example.com',
            password='pass123'
        )
        
        data = self.registration_data.copy()
        data['email'] = 'existing@example.com'
        response = self.client.post('/api/auth/register/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_success(self):
        """
        Test successful login.
        """
        user = CustomUser.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        user.is_active = True
        user.save()

        response = self.client.post('/api/auth/login/', {
            'username': 'testuser',
            'password': 'testpass123'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('message', response.data)

    def test_login_invalid_credentials(self):
        """
        Test login with invalid credentials.
        """
        response = self.client.post('/api/auth/login/', {
            'username': 'nonexistent',
            'password': 'wrongpass'
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_email_verification(self):
        """
        Test email verification endpoint.
        """
        user = CustomUser.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        registration = Registration.objects.create(
            user=user,
            confirmation_token='test-token-123'
        )

        response = self.client.get(f'/api/auth/verify-email/test-token-123/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Refresh objects from database
        registration.refresh_from_db()
        user.refresh_from_db()
        
        self.assertEqual(registration.status, 'confirmed')
        self.assertTrue(registration.is_email_verified)
        self.assertTrue(user.is_active)

    def test_password_reset_request(self):
        """
        Test password reset request.
        """
        user = CustomUser.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

        response = self.client.post('/api/auth/password-reset/', {
            'email': 'test@example.com'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check if password reset token was created
        self.assertTrue(PasswordReset.objects.filter(user=user, is_used=False).exists())

    def test_password_reset_confirm(self):
        """
        Test password reset confirmation.
        """
        user = CustomUser.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        password_reset = PasswordReset.objects.create(
            user=user,
            token='reset-token-123',
            expires_at=timezone.now() + timezone.timedelta(hours=1)
        )

        response = self.client.post('/api/auth/password-reset-confirm/', {
            'token': 'reset-token-123',
            'new_password': 'newstrongpass123',
            'confirm_password': 'newstrongpass123'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verify password was changed
        user.refresh_from_db()
        self.assertTrue(user.check_password('newstrongpass123'))

    def test_user_profile_access(self):
        """
        Test user profile access and update.
        """
        user = CustomUser.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        # Create profile
        profile = UserProfile.objects.create(user=user)
        
        # Force authenticate
        self.client.force_authenticate(user=user)
        
        # Test profile retrieval
        response = self.client.get('/api/auth/profile/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Test profile update
        response = self.client.patch('/api/auth/profile/', {
            'bio': 'This is my bio',
            'gender': 'M'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        profile.refresh_from_db()
        self.assertEqual(profile.bio, 'This is my bio')
        self.assertEqual(profile.gender, 'M')


class RegistrationSerializerTests(TestCase):
    """
    Test cases for registration serializers.
    """

    def test_registration_serializer_valid_data(self):
        """
        Test serializer with valid data.
        """
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'first_name': 'New',
            'last_name': 'User',
            'password': 'strongpass123',
            'confirm_password': 'strongpass123'
        }
        serializer = RegistrationSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_registration_serializer_password_mismatch(self):
        """
        Test serializer with mismatched passwords.
        """
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'strongpass123',
            'confirm_password': 'differentpass'
        }
        serializer = RegistrationSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('password', serializer.errors)
