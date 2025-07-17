#!/usr/bin/env python3
"""
Simple test script to verify user operations work correctly
Run this after starting the backend server
"""

import requests
import json

BASE_URL = "http://localhost:5000"

def test_admin_login():
    """Test admin login and get token"""
    response = requests.post(f"{BASE_URL}/api/admin/login", 
                           json={"password": "admin123"})
    if response.status_code == 200:
        token = response.json()['access_token']
        print("✅ Admin login successful")
        return token
    else:
        print("❌ Admin login failed:", response.json())
        return None

def test_user_operations(token):
    """Test user CRUD operations"""
    headers = {"Authorization": f"Bearer {token}"}
    
    # Test getting users
    print("\n🔍 Testing get users...")
    response = requests.get(f"{BASE_URL}/api/admin/users", headers=headers)
    if response.status_code == 200:
        users = response.json()['users']
        print(f"✅ Got {len(users)} users")
        return users
    else:
        print("❌ Get users failed:", response.json())
        return []

def test_user_deletion(token, user_id):
    """Test user deletion"""
    headers = {"Authorization": f"Bearer {token}"}
    
    print(f"\n🗑️ Testing delete user {user_id}...")
    response = requests.delete(f"{BASE_URL}/api/admin/users/{user_id}", headers=headers)
    
    if response.status_code == 200:
        print("✅ User deletion successful:", response.json())
        return True
    else:
        print("❌ User deletion failed:", response.json())
        return False

def test_debug_endpoint(token):
    """Test the debug endpoint"""
    headers = {"Authorization": f"Bearer {token}"}
    
    print("\n🔧 Testing debug endpoint...")
    response = requests.get(f"{BASE_URL}/api/admin/test-user-ops", headers=headers)
    
    if response.status_code == 200:
        debug_info = response.json()
        print("✅ Debug info:")
        for key, value in debug_info.items():
            print(f"   {key}: {value}")
        return True
    else:
        print("❌ Debug endpoint failed:", response.json())
        return False

def main():
    print("🚀 Starting user operations test...")
    
    # Test admin login
    token = test_admin_login()
    if not token:
        return
    
    # Test debug endpoint
    test_debug_endpoint(token)
    
    # Test getting users
    users = test_user_operations(token)
    
    # If there are users, test deletion (be careful!)
    if users and len(users) > 0:
        print(f"\n⚠️ Found {len(users)} users. Testing deletion is disabled by default.")
        print("To test deletion, uncomment the line below and specify a test user ID")
        # test_user_deletion(token, "test_user_id")  # Uncomment to test deletion
    
    print("\n✅ Test completed!")

if __name__ == "__main__":
    main()