#!/bin/bash

python manage.py makemigrations app
python manage.py migrate
python manage.py createsuperuser --username admin --email your_email@example.com --password password

exec python manage.py runserver 0.0.0.0:8000
