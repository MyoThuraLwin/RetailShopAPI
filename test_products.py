#!/usr/bin/env python
"""
Test script for Product Creation API
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

def test_product_creation():
    """Test product creation endpoints"""
    
    # Base URL (adjust as needed)
    base_url = "http://localhost:8000"
    
    print("🧪 Testing Product Creation API")
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
    
    # Test 2: Create a product category
    print("\n2. Creating product category...")
    category_data = {
        "name": "Electronics",
        "description": "Electronic devices and accessories"
    }
    
    response = requests.post(f"{base_url}/api/categories/", json=category_data, headers=headers)
    if response.status_code == 201:
        category = response.json()
        print(f"✅ Category created: {category['name']}")
        category_id = category['id']
    else:
        print(f"❌ Category creation failed: {response.text}")
        category_id = None
    
    # Test 3: Create a product
    print("\n3. Creating product...")
    product_data = {
        "name": "Wireless Bluetooth Headphones",
        "description": "High-quality wireless headphones with noise cancellation and 30-hour battery life.",
        "sku": "WBH-001",
        "barcode": "1234567890123",
        "price": "79.99",
        "compare_price": "99.99",
        "cost": "45.00",
        "weight": "0.35",
        "dimensions": "18 x 15 x 8 cm",
        "condition": "new",
        "status": "active",
        "stock_quantity": 50,
        "reorder_level": 10,
        "track_inventory": True,
        "category": category_id,
        "slug": "wireless-bluetooth-headphones",
        "meta_title": "Wireless Bluetooth Headphones - Best Sound Quality",
        "meta_description": "Premium wireless headphones with noise cancellation. Free shipping on orders over $50.",
        "tags": ["wireless", "bluetooth", "headphones", "audio"]
    }
    
    response = requests.post(f"{base_url}/api/products/", json=product_data, headers=headers)
    if response.status_code == 201:
        product = response.json()
        print(f"✅ Product created: {product['name']}")
        print(f"   SKU: {product['sku']}")
        print(f"   Price: ${product['price']}")
        print(f"   ID: {product['id']}")
        product_id = product['id']
    else:
        print(f"❌ Product creation failed: {response.text}")
        product_id = None
    
    # Test 4: List products
    print("\n4. Listing products...")
    response = requests.get(f"{base_url}/api/products/")
    if response.status_code == 200:
        products = response.json()
        print(f"✅ Found {len(products)} products")
        for product in products[:3]:  # Show first 3 products
            print(f"   - {product['name']} (${product['price']})")
    else:
        print(f"❌ Failed to list products: {response.text}")
    
    # Test 5: Get product details
    if product_id:
        print(f"\n5. Getting product details...")
        response = requests.get(f"{base_url}/api/products/{product_id}/")
        if response.status_code == 200:
            product = response.json()
            print(f"✅ Product details retrieved")
            print(f"   Name: {product['name']}")
            print(f"   Description: {product['description'][:100]}...")
            print(f"   Price: ${product['price']}")
            print(f"   Stock: {product['stock_quantity']}")
            print(f"   In Stock: {product['is_in_stock']}")
        else:
            print(f"❌ Failed to get product details: {response.text}")
    
    # Test 6: Search products
    print("\n6. Searching products...")
    search_params = {"q": "wireless"}
    response = requests.get(f"{base_url}/api/products/search/", params=search_params)
    if response.status_code == 200:
        results = response.json()
        print(f"✅ Search found {len(results.get('results', []))} results")
    else:
        print(f"❌ Search failed: {response.text}")
    
    # Test 7: Get featured products
    print("\n7. Getting featured products...")
    response = requests.get(f"{base_url}/api/products/featured/")
    if response.status_code == 200:
        featured = response.json()
        print(f"✅ Found {len(featured)} featured products")
    else:
        print(f"❌ Failed to get featured products: {response.text}")
    
    print("\n🎉 Product Creation API tests completed!")

if __name__ == "__main__":
    test_product_creation()
