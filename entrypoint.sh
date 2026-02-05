#!/bin/sh

echo "Running migrations..."
python manage.py migrate

echo "Creating Superuser"
python manage.py createsuperuser --no-input || echo "Superuser already exists or failed to create"

echo "Building TailwindCSS"
npm run build

echo "Starting server..."
python manage.py runserver 0.0.0.0:8000