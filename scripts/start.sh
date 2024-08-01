#!/bin/sh

# Start Gunicorn
gunicorn core.wsgi --bind 0.0.0.0:4001

# Run Django management commands
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic

