import os
from pika import PlainCredentials, ConnectionParameters, BlockingConnection

MQ_USERNAME = os.environ.get("MQ_USERNAME", "guest")
MQ_PASSWORD = os.environ.get("MQ_PASSWORD", "guest")
MQ_ADDRESS = os.environ.get("MQ_ADDRESS", "localhost")
MQ_PORT = os.environ.get("MQ_PORT", 5672)


def setup_mq_connections(exchange_name, queue_name, routing_key):
    try:
        credentials = PlainCredentials(MQ_USERNAME, MQ_PASSWORD)
        connection_params = ConnectionParameters(MQ_ADDRESS, MQ_PORT, "/", credentials)
        connection = BlockingConnection(connection_params)
        channel = connection.channel()
        print(f"Connected to RabbitMQ: {connection}")

        channel.exchange_declare(exchange=exchange_name, exchange_type="direct")
        channel.queue_declare(queue=queue_name)
        channel.queue_bind(
            exchange=exchange_name,
            queue=queue_name,
            routing_key=routing_key,
        )
        return channel
    except Exception as e:
        print(f"Error connecting to RabbitMQ: {e}")
        raise e
