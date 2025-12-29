#!/bin/bash
set -e

echo "Starting Kwiz backend..."

# Collect static files
python manage.py collectstatic --noinput

# Run migrations
python manage.py migrate

# Set admin password (creates fresh admin user)
python manage.py set_admin_password

# Start gunicorn
exec gunicorn kwiz_project.wsgi --bind 0.0.0.0:$PORT --workers 2
