#!/bin/bash
# Function to check if RabbitMQ is up
echo "Waiting for RabbitMQ to start..."
while ! nc -z rabbitmq 5672; do
    sleep 1
done
echo "RabbitMQ started"

