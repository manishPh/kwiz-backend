web: python manage.py collectstatic --noinput && python manage.py migrate && gunicorn kwiz_project.wsgi --bind 0.0.0.0:$PORT
