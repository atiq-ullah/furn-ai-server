import os
import pika
from dotenv import load_dotenv


load_dotenv()
address = os.environ.get("IP")
address = "localhost" if address is None else address


class SignalConnection:
    def __init__(self):
        self.channel = None

    def connect_to_rabbitmq(
        self, username, password, connection_address=address, connection_port=5672
    ):
        credentials = pika.PlainCredentials(username, password)
        try:
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(
                    connection_address, connection_port, "/", credentials
                )
            )
            print(f"Connected to RabbitMQ: {connection}")
            return connection
        except Exception as e:  # pylint: disable=broad-except
            print(f"Error connecting to RabbitMQ: {e}")
            return None

    def setup_channel(self, connection, exchange_name, queue_name, routing_key):
        try:
            self.channel = connection.channel()
            self.channel.exchange_declare(
                exchange=exchange_name, exchange_type="direct"
            )
            self.channel.queue_declare(queue=queue_name)
            self.channel.queue_bind(
                exchange=exchange_name,
                queue=queue_name,
                routing_key=routing_key,
            )
            return self.channel
        except Exception as e:  # pylint: disable=broad-except
            print(f"Error setting up channel: {e}")
            return None
