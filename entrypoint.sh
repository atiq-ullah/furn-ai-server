#!/bin/bash
 python manage.py makemigrations app
# Apply database migrations
python manage.py migrate

# Start server
exec python manage.py runserver 0.0.0.0:8000
