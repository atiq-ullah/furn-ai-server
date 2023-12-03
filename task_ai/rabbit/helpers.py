import pika

connection = None
class Connection:
    def __init__(self):
        self.connection = None
            
    def connect(self):
        print("Attempting to connect to rabbitmq")
        try:
            self.connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
            channel = self.connection.channel()
            print(f"Connected!")

            return channel
        except Exception as e:
            print(f"Received an error trying to connect: {e}")

    def close_connection(self):
        self.connection.close()