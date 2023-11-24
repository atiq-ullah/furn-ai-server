#!/bin/bash

python manage.py makemigrations app
python manage.py migrate

exec celery -A task_ai.app.handlers worker --loglevel=info
