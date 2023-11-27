import os
import pika
from dotenv import load_dotenv


class SignalConnection:
    def __init__(self, username, password, connection_address="localhost", connection_port=5672):
        self.connection = None
        self.channel = None

        credentials = pika.PlainCredentials(username, password)
        try:
            self.connection = pika.BlockingConnection(
                pika.ConnectionParameters(
                    connection_address, connection_port, "/", credentials
                )
            )
            print(f"Connected to RabbitMQ: {self.connection}")
            self.channel = self.connection.channel()
        except Exception as e:  # pylint: disable=broad-except
            print(f"Error connecting to RabbitMQ: {e}")
            raise e

    def setup_channel(self, exchange_name, queue_name, routing_key):
        try:
            if self.channel is None:
                return None
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
