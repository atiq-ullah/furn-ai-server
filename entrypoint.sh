#!/bin/bash
# Function to check if RabbitMQ is up
wait_for_rabbitmq() {
    echo "Waiting for RabbitMQ to start..."
    while ! nc -z rabbitmq 5672; do
      sleep 1
    done
    echo "RabbitMQ started"
}

# Call the function to wait for RabbitMQ
wait_for_rabbitmq
python manage.py makemigrations app
python manage.py migrate

exec python manage.py runserver 0.0.0.0:8000
