from rich.console import Console
import requests
from requests.auth import HTTPBasicAuth
import pika

from dotenv import load_dotenv

load_dotenv()

console = Console()
credentials = pika.PlainCredentials("guest", "guest")

connection_address = "34.134.37.153"
address = connection_address
connection_port = 5672
url = "http://" + address + ":8000/prompt"
username = "admin"
password = "password"
connection = pika.BlockingConnection(
    pika.ConnectionParameters(address, connection_port, "/", credentials)
)
parse_channel = connection.channel()
cat_channel = connection.channel()

test_content = "Wash the dishes, go to the store, and take out the trash."


def main():
    console.print("\n[bold blue]Task AI[/bold blue]\n")

    console.print("[bold red]Enter a prompt: [/bold red]")
    # text = input()
    console.print("[bold red]Processing... [/bold red]\n")
    data = {"prompt": test_content, "p_type": "parse"}

    console.print("Parsing...")
    # TODO: Error handling
    response = requests.post(
        url, data=data, auth=HTTPBasicAuth(username, password), timeout=10
    )
    print(response.content)

    def cat_callback(ch, method, properties, body):  # pylint: disable=unused-argument
        message = body.decode("utf-8")
        print(f"\n\n{message}")
        parse_channel.stop_consuming()
        cat_channel.stop_consuming()
        return

    def parse_callback(ch, method, properties, body):  # pylint: disable=unused-argument
        message = body.decode("utf-8")
        data = {"prompt": message, "p_type": "cat"}
        console.print("Categorizing...")
        # TODO: Error handling
        response = requests.post(
            url, data=data, auth=HTTPBasicAuth(username, password), timeout=10
        )
        print(response.content)
        cat_channel.basic_consume(
            queue="prompt_cat", on_message_callback=cat_callback, auto_ack=True
        )
        return

    parse_channel.basic_consume(
        queue="prompt_parse", on_message_callback=parse_callback, auto_ack=True
    )
    parse_channel.start_consuming()


if __name__ == "__main__":
    main()
