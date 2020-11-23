#!/bin/bash
# Migrate the database first
echo "Migrating the database before starting the server"
python manage.py makemigrations
python manage.py migrate
DJANGO_SUPERUSER_PASSWORD=my_password python manage.py createsuperuser \
    --no-input \
    --email=my_user@domain.com
# Start Gunicorn processes
echo "Starting Gunicorn."
exec gunicorn relance_patient.wsgi:application \
    --bind 0.0.0.0:8888