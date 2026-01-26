#!/usr/bin/env bash

# Stop execution if any command fails
set -e

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Running migrations..."
python manage.py migrate --noinput

echo "Creating superuser..."
# This sends the python code directly into Django's management shell
# This is safe because it uses the loaded Django environment
python manage.py shell <<EOF
import os
from django.contrib.auth import get_user_model

User = get_user_model()
username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@example.com')
password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'admin123')

if not User.objects.filter(username=username).exists():
    print(f"Creating superuser: {username}")
    User.objects.create_superuser(username, email, password)
else:
    print("Superuser already exists.")
EOF

echo "Starting Gunicorn..."
exec python -m gunicorn --bind 0.0.0.0:8000 --workers 3 config.wsgi:application