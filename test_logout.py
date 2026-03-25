#!/usr/bin/env python
"""
Test script for JWT logout functionality
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

def test_logout_functionality():
    """Test the logout endpoint with various scenarios"""
    
    # Base URL (adjust as needed)
    base_url = "http://localhost:8000"
    
    print("🧪 Testing JWT Logout Functionality")
    print("=" * 50)
    
    # Test 1: Login to get tokens
    print("\n1. Testing login...")
    login_data = {
        "username": "testuser",
        "password": "testpass123"
    }
    
    try:
        response = requests.post(f"{base_url}/api/auth/login/", json=login_data)
        if response.status_code == 200:
            tokens = response.json()
            refresh_token = tokens.get('refresh_token')
            print(f"✅ Login successful")
            print(f"   Access Token: {tokens.get('access_token')[:50]}...")
            print(f"   Refresh Token: {refresh_token[:50]}...")
        else:
            print(f"❌ Login failed: {response.text}")
            return
    except requests.exceptions.ConnectionError:
        print("⚠️  Cannot connect to API. Make sure Django server is running on localhost:8000")
        return
    
    # Test 2: Successful logout
    print("\n2. Testing successful logout...")
    logout_data = {"refresh_token": refresh_token}
    
    response = requests.post(f"{base_url}/api/auth/logout/", json=logout_data)
    if response.status_code == 200:
        print("✅ Logout successful")
        print(f"   Response: {response.json()}")
    else:
        print(f"❌ Logout failed: {response.text}")
    
    # Test 3: Try to logout again with same token (should fail)
    print("\n3. Testing logout with already blacklisted token...")
    response = requests.post(f"{base_url}/api/auth/logout/", json=logout_data)
    if response.status_code == 400:
        print("✅ Correctly rejected blacklisted token")
        print(f"   Response: {response.json()}")
    else:
        print(f"❌ Should have rejected blacklisted token: {response.text}")
    
    # Test 4: Try logout with invalid token
    print("\n4. Testing logout with invalid token...")
    invalid_logout_data = {"refresh_token": "invalid.token.here"}
    
    response = requests.post(f"{base_url}/api/auth/logout/", json=invalid_logout_data)
    if response.status_code == 400:
        print("✅ Correctly rejected invalid token")
        print(f"   Response: {response.json()}")
    else:
        print(f"❌ Should have rejected invalid token: {response.text}")
    
    # Test 5: Try logout without token
    print("\n5. Testing logout without token...")
    response = requests.post(f"{base_url}/api/auth/logout/", json={})
    if response.status_code == 400:
        print("✅ Correctly required refresh token")
        print(f"   Response: {response.json()}")
    else:
        print(f"❌ Should have required refresh token: {response.text}")
    
    print("\n🎉 Logout functionality tests completed!")

if __name__ == "__main__":
    test_logout_functionality()
