#!/usr/bin/env python
"""
Test authentication for admin user
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kwiz_project.settings')
django.setup()

from django.contrib.auth import authenticate, get_user_model

User = get_user_model()

print("=" * 60)
print("TESTING ADMIN AUTHENTICATION")
print("=" * 60)

# Test credentials
username = 'admin'
password = 'admin123'

print(f"\nTesting login with:")
print(f"  Username: {username}")
print(f"  Password: {password}")

# Get user
try:
    user = User.objects.get(username=username)
    print(f"\n✓ User found in database")
    print(f"  Email: {user.email}")
    print(f"  Is active: {user.is_active}")
    print(f"  Is staff: {user.is_staff}")
    print(f"  Is superuser: {user.is_superuser}")
    
    # Test password
    if user.check_password(password):
        print(f"\n✓ Password check: PASSED")
    else:
        print(f"\n✗ Password check: FAILED")
        print(f"  The password '{password}' does not match the stored password")
    
    # Test authentication
    auth_user = authenticate(username=username, password=password)
    if auth_user:
        print(f"\n✓ Django authenticate(): SUCCESS")
        print(f"  Authenticated as: {auth_user.username}")
    else:
        print(f"\n✗ Django authenticate(): FAILED")
        print(f"  Authentication returned None")
        
except User.DoesNotExist:
    print(f"\n✗ User '{username}' not found in database")

print("\n" + "=" * 60)

