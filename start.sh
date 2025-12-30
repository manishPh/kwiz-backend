#!/bin/bash
set -e

echo "Starting Kwiz backend..."

# Collect static files
python manage.py collectstatic --noinput

# Run migrations
python manage.py migrate

# Create admin user
echo "Creating admin user..."
python create_admin_simple.py || echo "Admin user creation failed, continuing..."

# Start gunicorn
exec gunicorn kwiz_project.wsgi --bind 0.0.0.0:$PORT --workers 2
