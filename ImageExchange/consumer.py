import os
import time
import pika
import pdb
from PIL import Image


class Consumer:
    def __init__(self, exchange_name, queue_name, routing_key):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        self.channel = self.connection.channel()
        self.channel.basic_qos(prefetch_count=1)
        self.channel.queue_declare(queue=queue_name, durable=True)
        self.channel.queue_bind(exchange=exchange_name, queue=queue_name, routing_key=routing_key)
        self.queue_name = queue_name

    def __del__(self):
        self.connection.close()

    def receive_images(self):
        for method, properties, body in self.channel.consume(queue=self.queue_name):
            filename = body.decode('utf-8')
            image = Image.open(filename)
            print("Image = ", image)
            self.channel.basic_ack(delivery_tag=method.delivery_tag)
            # delete image here
            os.remove(filename)
            return image
