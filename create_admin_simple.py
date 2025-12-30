#!/usr/bin/env python
"""
Simple script to create admin user in PostgreSQL
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kwiz_project.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# Delete all existing users first
print("Deleting existing users...")
User.objects.all().delete()

# Create admin user
print("Creating admin user...")
admin = User.objects.create_superuser(
    username='admin',
    email='admin@kwiz.fun',
    password='admin123'
)

print(f"✓ Admin user created successfully!")
print(f"  Username: admin")
print(f"  Password: admin123")
print(f"  Email: {admin.email}")

# Verify
if admin.check_password('admin123'):
    print("✓ Password verification: PASSED")
else:
    print("✗ Password verification: FAILED")

# List all users
print("\nAll users in database:")
for user in User.objects.all():
    print(f"  - {user.username} (staff: {user.is_staff}, super: {user.is_superuser})")

