#!/bin/bash
set -e

echo "Starting Kwiz backend..."

# Collect static files
python manage.py collectstatic --noinput

# Run migrations
python manage.py migrate

# Create admin user if it doesn't exist
python create_admin.py

# Start gunicorn
exec gunicorn kwiz_project.wsgi --bind 0.0.0.0:$PORT --workers 2
