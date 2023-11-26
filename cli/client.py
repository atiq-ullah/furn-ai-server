from rich.console import Console
import requests
from requests.auth import HTTPBasicAuth
import pika
import asyncio
import threading
# from socketio_server import sio  # Ensure this is the correct import

from dotenv import load_dotenv

load_dotenv()
# sio.emit("result", "Hello World")

import socketio
import asyncio

sio = socketio.AsyncServer(async_mode='asgi')
app = socketio.ASGIApp(sio)



@sio.event
async def connect(sid, environ):
    print('Socket.IO client connected:', sid)

@sio.event
async def disconnect(sid):
    print('Socket.IO client disconnected:', sid)


def emit_sync(event, message):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(sio.emit(event, message))
    loop.close()

# Usage


def main():
    emit_sync("result", "Hello World")

# console = Console()
# credentials = pika.PlainCredentials("guest", "guest")

# connection_address = "34.134.37.153"
# address = connection_address
# connection_port = 5672
# url = "http://" + address + ":8000/prompt"
# username = "admin"
# password = "password"
# connection = pika.BlockingConnection(
#     pika.ConnectionParameters(address, connection_port, "/", credentials)
# )
# parse_channel = connection.channel()
# cat_channel = connection.channel()

# test_content = "Washes the dishes, do homework, and go to bed."

# # def emit_async(message):
#     # asyncio.run(sio.emit("result", message))

# def cat_callback(ch, method, properties, body):  # pylint: disable=unused-argument
#     message = body.decode("utf-8")
#     print(f"\n\n{message}")

#     # Start the emit in a separate thread
#     # threading.Thread(target=emit_async, args=(message,)).start()
#     sio.emit("result", message)

#     parse_channel.stop_consuming()
#     cat_channel.stop_consuming()

# def parse_callback(ch, method, properties, body):  # pylint: disable=unused-argument
#     message = body.decode("utf-8")
#     data = {"prompt": message, "p_type": "cat"}
#     console.print("Categorizing...")
#     response = requests.post(
#         url, data=data, auth=HTTPBasicAuth(username, password), timeout=30
#     )
#     print(response.content)
#     cat_channel.basic_consume(
#         queue="prompt_cat", on_message_callback=cat_callback, auto_ack=True
#     )

# def main():
#     console.print("\n[bold blue]Task AI[/bold blue]\n")

#     console.print("[bold red]Enter a prompt: [/bold red]")
#     console.print("[bold red]Processing... [/bold red]\n")
#     data = {"prompt": test_content, "p_type": "parse"}

#     console.print("Parsing...")
#     response = requests.post(
#         url, data=data, auth=HTTPBasicAuth(username, password), timeout=30
#     )
#     print(response.content)

#     parse_channel.basic_consume(
#         queue="prompt_parse", on_message_callback=parse_callback, auto_ack=True
#     )
#     parse_channel.start_consuming()

if __name__ == "__main__":
    main()
