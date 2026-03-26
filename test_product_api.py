from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from decimal import Decimal
from products.models import Product

User = get_user_model()


class ProductAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.admin_user = User.objects.create_user(
            username='admin',
            email='admin@example.com',
            password='adminpass123',
            is_staff=True,
            is_superuser=True
        )
        
        # Create test product
        self.product = Product.objects.create(
            product_code='TEST001',
            name='Test Product',
            description='This is a test product',
            price=Decimal('99.99'),
            created_by=self.admin_user
        )

    def test_list_products(self):
        """Test GET /api/products/"""
        response = self.client.get('/api/products/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_create_product_unauthorized(self):
        """Test POST /api/products/ without authentication"""
        data = {
            'product_code': 'TEST002',
            'name': 'New Product',
            'description': 'A new test product',
            'price': '49.99'
        }
        response = self.client.post('/api/products/', data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_product_authorized(self):
        """Test POST /api/products/ with admin user"""
        self.client.force_authenticate(user=self.admin_user)
        data = {
            'product_code': 'TEST002',
            'name': 'New Product',
            'description': 'A new test product',
            'price': '49.99'
        }
        response = self.client.post('/api/products/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 2)

    def test_retrieve_product(self):
        """Test GET /api/products/{id}/"""
        response = self.client.get(f'/api/products/{self.product.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['product_code'], 'TEST001')

    def test_update_product(self):
        """Test PUT /api/products/{id}/"""
        self.client.force_authenticate(user=self.admin_user)
        data = {
            'product_code': 'TEST001',
            'name': 'Updated Product',
            'description': 'Updated description',
            'price': '149.99'
        }
        response = self.client.put(f'/api/products/{self.product.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.product.refresh_from_db()
        self.assertEqual(self.product.name, 'Updated Product')

    def test_delete_product(self):
        """Test DELETE /api/products/{id}/"""
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.delete(f'/api/products/{self.product.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Product.objects.count(), 0)

    def test_search_products(self):
        """Test GET /api/products/search/"""
        response = self.client.get('/api/products/search/?q=Test')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_product_code_unique_validation(self):
        """Test that product codes must be unique"""
        self.client.force_authenticate(user=self.admin_user)
        data = {
            'product_code': 'TEST001',  # Same as existing product
            'name': 'Duplicate Product',
            'description': 'This should fail',
            'price': '29.99'
        }
        response = self.client.post('/api/products/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('product_code', response.data)
