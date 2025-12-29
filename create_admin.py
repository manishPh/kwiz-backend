#!/usr/bin/env python
"""
Create or reset admin superuser for Railway deployment
Run this with: railway run python create_admin.py
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kwiz_project.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# Configuration
USERNAME = 'admin'
EMAIL = 'admin@kwiz.fun'
PASSWORD = 'admin123'  # Change this to a secure password

print("=" * 60)
print("KWIZ ADMIN USER SETUP")
print("=" * 60)

# List existing users
print("\nExisting users:")
for user in User.objects.all():
    print(f"  - {user.username} (email: {user.email}, staff: {user.is_staff}, super: {user.is_superuser})")

# Try to get or create admin user
try:
    user = User.objects.get(username=USERNAME)
    print(f"\nUser '{USERNAME}' already exists. Updating...")
    user.email = EMAIL
    user.set_password(PASSWORD)
    user.is_staff = True
    user.is_superuser = True
    user.is_active = True
    user.save()
    print(f"✓ Updated user '{USERNAME}'")
except User.DoesNotExist:
    print(f"\nCreating new user '{USERNAME}'...")
    user = User.objects.create_superuser(
        username=USERNAME,
        email=EMAIL,
        password=PASSWORD
    )
    print(f"✓ Created superuser '{USERNAME}'")

print("\n" + "=" * 60)
print("ADMIN CREDENTIALS:")
print("=" * 60)
print(f"Username: {USERNAME}")
print(f"Email: {EMAIL}")
print(f"Password: {PASSWORD}")
print("=" * 60)
print("\nYou can now login at: https://web-production-28c98.up.railway.app/admin/")
print("\n⚠️  IMPORTANT: Change the password after first login!")
print("=" * 60)

