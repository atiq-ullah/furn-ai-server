from rich.console import Console
from rich.markdown import Markdown
from rich.prompt import Prompt
import requests
from requests.auth import HTTPBasicAuth
import pika

console = Console()


def main():
    console.print("\n[bold blue]Welcome to Your CLI Markdown Formatter![/bold blue]\n")

    credentials = pika.PlainCredentials("guest", "guest")
    queue_name = "prompt_cat"
    exchange_name = "prompt"
    routing_key = "request.cat"
    connection_address = "localhost"
    connection_port = 5672

    connection = pika.BlockingConnection(
        pika.ConnectionParameters(connection_address, connection_port, "/", credentials)
    )

    text = input("Enter text: ")
    console.print(text)

    # Your endpoint
    url = "http://0.0.0.0:8000/prompt"

    # Basic Auth credentials
    username = "admin"
    password = "password"

    # Data to be sent in x-www-form-urlencoded format
    data = {"prompt": text, "p_type": "parse"}

    # Make the POST request with basic authentication
    response = requests.post(url, data=data, auth=HTTPBasicAuth(username, password))

    # Get the response (for example, as text)
    console.print(response.text)
    count = 0
    channel = connection.channel()
    channel_cat = connection.channel()

    def callback(ch, method, properties, body):  # pylint: disable=unused-argument
        message = body.decode("utf-8")
        print(f"PARSED message: \n{message}")

        data = {"prompt": message, "p_type": "cat"}
        response = requests.post(url, data=data, auth=HTTPBasicAuth(username, password))
        console.print("CAT: ", response.text)

        channel_cat.basic_consume(
            queue="prompt_cat", on_message_callback=cat_callback, auto_ack=True
        )
        # channel_cat.start_consuming()

        return response.text

    def cat_callback(ch, method, properties, body):  # pylint: disable=unused-argument
        message = body.decode("utf-8")
        print(f"CATEGORIZED message: \n{message}")
        return response.text

    channel.basic_consume(
        queue="prompt_parse", on_message_callback=callback, auto_ack=True
    )
    channel.start_consuming()

    # print(
    #     f"Waiting for messages in the queue {queue_name}. To exit, press Ctrl+C."
    # )

    # Send HTTP request to my API
    # Wait for rabbitmq message
    # Send another request with the message
    # Wait for response
    # Display response


if __name__ == "__main__":
    main()
