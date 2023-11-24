import pika


def connect_to_rabbitmq():
    try:
        credentials = pika.PlainCredentials("guest", "guest")
        connection = pika.BlockingConnection(
            pika.ConnectionParameters("0.0.0.0", 5672, "/", credentials)
        )
        return connection
    except Exception as e:
        print(f"Error connecting to RabbitMQ: {e}")
        return None


def create_exchange(channel, exchange_name):
    try:
        channel.exchange_declare(exchange=exchange_name, exchange_type="direct")
        print(f"Created exchange: {exchange_name}")
    except Exception as e:
        print(f"Error creating exchange: {e}")


def create_queue(channel, queue_name):
    try:
        channel.queue_declare(queue=queue_name)
        print(f"Created queue: {queue_name}")
    except Exception as e:
        print(f"Error creating queue: {e}")


def bind_queue_to_exchange(channel, exchange_name, queue_name, routing_key):
    try:
        channel.queue_bind(
            exchange=exchange_name, queue=queue_name, routing_key=routing_key
        )
        print(
            f"Bound queue {queue_name} to exchange {exchange_name} with routing key {routing_key}"
        )
    except Exception as e:
        print(f"Error binding queue to exchange: {e}")


def publish_message(channel, exchange_name, routing_key, message):
    try:
        channel.basic_publish(
            exchange=exchange_name, routing_key=routing_key, body=message
        )
        print(f"Published message: {message}")
    except Exception as e:
        print(f"Error publishing message: {e}")


def consume_message(channel, queue_name):
    def callback(ch, method, properties, body):
        message = body.decode("utf-8")
        print(f"Received message: {message}")
        # Process the message here

    try:
        channel.basic_consume(
            queue=queue_name, on_message_callback=callback, auto_ack=True
        )
        print(f"Waiting for messages in the queue {queue_name}. To exit, press Ctrl+C.")
        channel.start_consuming()
    except Exception as e:
        print(f"Error consuming messages: {e}")


if __name__ == "__main__":
    connection = connect_to_rabbitmq()
    if connection:
        channel = connection.channel()

        # Customize exchange, queue, and routing key names as needed
        queue_name = "my_queue"
        exchange_name = "my_exchange"
        routing_key = "my_routing_key"
        create_exchange(channel, exchange_name)
        create_queue(channel, queue_name)
        bind_queue_to_exchange(channel, exchange_name, queue_name, routing_key)

        # Example usage: Publish a message
        publish_message(channel, exchange_name, routing_key, 'Hello, RabbitMQ!')


        publish_message(channel, exchange_name, routing_key, 'Hello, Again!')

        # Start consuming messages
        consume_message(channel, queue_name)