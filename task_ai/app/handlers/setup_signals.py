import pika


class SignalConnection:
    def __init__(self):
        self.credentials = pika.PlainCredentials("guest", "guest")
        self.queue_name = "prompt"
        self.exchange_name = "prompt"
        self.routing_key = "prompt"
        self.connection_address = "rabbitmq"
        self.connection_port = 5672

        self.connection = self.connect_to_rabbitmq()
        print(f"Connected to RabbitMQ: {self.connection}")
        self.channel = self.connection.channel()

    def connect_to_rabbitmq(self):
        try:
            connection_obj = pika.BlockingConnection(
                pika.ConnectionParameters(
                    self.connection_address, self.connection_port, "/", self.credentials
                )
            )
            return connection_obj
        except Exception as e:  # pylint: disable=broad-except
            print(f"Error connecting to RabbitMQ: {e}")
            return None

    def create_exchange(self):
        try:
            self.channel.exchange_declare(
                exchange=self.exchange_name, exchange_type="direct"
            )
            print(f"Created exchange: {self.exchange_name}")
        except Exception as e:  # pylint: disable=broad-except
            print(f"Error creating exchange: {e}")

    def create_queue(self):
        try:
            self.channel.queue_declare(queue=self.queue_name)
            print(f"Created queue: {self.queue_name}")
        except Exception as e:  # pylint: disable=broad-except
            print(f"Error creating queue: {e}")

    def bind_queue_to_exchange(self):
        try:
            self.channel.queue_bind(
                exchange=self.exchange_name,
                queue=self.queue_name,
                routing_key=self.routing_key,
            )
            print(
                f"Bound queue {self.queue_name} to exchange {self.exchange_name} with routing key {self.routing_key}"
            )
        except Exception as e:  # pylint: disable=broad-except
            print(f"Error binding queue to exchange: {e}")

    def publish_message(self, message):
        try:
            self.channel.basic_publish(
                exchange=self.exchange_name, routing_key=self.routing_key, body=message
            )
            print(f"Published message: {message}")
        except Exception as e:  # pylint: disable=broad-except
            print(f"Error publishing message: {e}")

    def consume_message(self):
        def callback(ch, method, properties, body):  # pylint: disable=unused-argument
            message = body.decode("utf-8")
            print(f"Received message: {message}")
            # Process the message here

        try:
            self.channel.basic_consume(
                queue=self.queue_name, on_message_callback=callback, auto_ack=True
            )
            print(
                f"Waiting for messages in the queue {self.queue_name}. To exit, press Ctrl+C."
            )
            self.channel.start_consuming()
        except Exception as e:  # pylint: disable=broad-except
            print(f"Error consuming messages: {e}")

if __name__ == "__main__":
    conn = SignalConnection()
    conn.create_exchange()
    conn.create_queue()
    conn.bind_queue_to_exchange()
    conn.publish_message("Hello World!")
    conn.consume_message()


