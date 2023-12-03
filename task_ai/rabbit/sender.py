from helpers import Connection

print("Hello, from the server!")
connection = Connection()
channel = connection.connect()
channel.queue_declare(queue='bunny')
channel.basic_publish(exchange='',
                      routing_key='bunny',
                      body='Hello World!')
print(" [x] Sent 'Hello World!'")

connection.close_connection()
