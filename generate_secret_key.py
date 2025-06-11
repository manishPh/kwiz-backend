#!/usr/bin/env python3
"""
Generate a secure Django secret key for production use.
Run this script and copy the output to your Railway environment variables.
"""

import secrets
import string

def generate_secret_key(length=50):
    """Generate a secure secret key for Django."""
    alphabet = string.ascii_letters + string.digits + '!@#$%^&*(-_=+)'
    return ''.join(secrets.choice(alphabet) for _ in range(length))

if __name__ == "__main__":
    secret_key = generate_secret_key()
    print("=" * 60)
    print("DJANGO SECRET KEY FOR PRODUCTION")
    print("=" * 60)
    print(f"SECRET_KEY={secret_key}")
    print("=" * 60)
    print("Copy the SECRET_KEY value above to your Railway environment variables")
    print("=" * 60)
