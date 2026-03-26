#!/usr/bin/env python
"""
Test script for Simplified Product Creation API
"""
import os
import sys
import django
import requests
import json

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'RetailShopAPI.settings')
django.setup()

from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

def test_simplified_product_creation():
    """Test simplified product creation endpoints"""
    
    # Base URL (adjust as needed)
    base_url = "http://localhost:8000"
    
    print("🧪 Testing Simplified Product Creation API")
    print("=" * 50)
    
    # Test 1: Login to get tokens (need admin/staff access)
    print("\n1. Testing admin login...")
    login_data = {
        "username": "admin",  # Replace with actual admin username
        "password": "admin123"  # Replace with actual admin password
    }
    
    try:
        response = requests.post(f"{base_url}/api/auth/login/", json=login_data)
        if response.status_code == 200:
            tokens = response.json()
            access_token = tokens.get('access_token')
            print(f"✅ Admin login successful")
            headers = {
                'Authorization': f'Bearer {access_token}',
                'Content-Type': 'application/json'
            }
        else:
            print(f"❌ Admin login failed: {response.text}")
            print("⚠️  Please create an admin user first:")
            print("   .venv\\Scripts\\python.exe manage.py createsuperuser")
            return
    except requests.exceptions.ConnectionError:
        print("⚠️  Cannot connect to API. Make sure Django server is running on localhost:8000")
        return
    
    # Test 2: Create a simplified product
    print("\n2. Creating simplified product...")
    product_data = {
        "product_code": "PROD-001",
        "name": "Sample Product",
        "description": "This is a sample product description for testing purposes.",
        "price": "29.99"
    }
    
    response = requests.post(f"{base_url}/api/products/", json=product_data, headers=headers)
    if response.status_code == 201:
        product = response.json()
        print(f"✅ Product created successfully!")
        print(f"   ID: {product['id']}")
        print(f"   Product Code: {product['product_code']}")
        print(f"   Name: {product['name']}")
        print(f"   Price: ${product['price']}")
        print(f"   Created By: {product['created_by']}")
        print(f"   Created At: {product['created_at']}")
        product_id = product['id']
    else:
        print(f"❌ Product creation failed: {response.text}")
        product_id = None
    
    # Test 3: List all products
    print("\n3. Listing all products...")
    response = requests.get(f"{base_url}/api/products/")
    if response.status_code == 200:
        products = response.json()
        print(f"✅ Found {len(products)} products")
        for product in products:
            print(f"   - {product['name']} (${product['price']}) - Code: {product['product_code']}")
    else:
        print(f"❌ Failed to list products: {response.text}")
    
    # Test 4: Get product details
    if product_id:
        print(f"\n4. Getting product details...")
        response = requests.get(f"{base_url}/api/products/{product_id}/")
        if response.status_code == 200:
            product = response.json()
            print(f"✅ Product details retrieved:")
            print(f"   ID: {product['id']}")
            print(f"   Product Code: {product['product_code']}")
            print(f"   Name: {product['name']}")
            print(f"   Description: {product['description'][:50]}...")
            print(f"   Price: ${product['price']}")
            print(f"   Created By: {product['created_by']}")
            print(f"   Updated By: {product['updated_by']}")
            print(f"   Created At: {product['created_at']}")
            print(f"   Updated At: {product['updated_at']}")
        else:
            print(f"❌ Failed to get product details: {response.text}")
    
    # Test 5: Update product
    if product_id:
        print(f"\n5. Updating product...")
        update_data = {
            "name": "Updated Sample Product",
            "price": "39.99",
            "description": "This is an updated product description."
        }
        
        response = requests.patch(f"{base_url}/api/products/{product_id}/", json=update_data, headers=headers)
        if response.status_code == 200:
            product = response.json()
            print(f"✅ Product updated successfully!")
            print(f"   New Name: {product['name']}")
            print(f"   New Price: ${product['price']}")
            print(f"   Updated By: {product['updated_by']}")
        else:
            print(f"❌ Product update failed: {response.text}")
    
    # Test 6: Search products
    print("\n6. Searching products...")
    search_params = {"q": "sample"}
    response = requests.get(f"{base_url}/api/products/search/", params=search_params)
    if response.status_code == 200:
        results = response.json()
        print(f"✅ Search found {len(results.get('results', []))} results")
    else:
        print(f"❌ Search failed: {response.text}")
    
    # Test 7: Filter by price range
    print("\n7. Filtering products by price range...")
    filter_params = {"min_price": "20", "max_price": "50"}
    response = requests.get(f"{base_url}/api/products/", params=filter_params)
    if response.status_code == 200:
        products = response.json()
        print(f"✅ Found {len(products)} products in price range $20-$50")
    else:
        print(f"❌ Price filter failed: {response.text}")
    
    print("\n🎉 Simplified Product Creation API tests completed!")

if __name__ == "__main__":
    test_simplified_product_creation()
