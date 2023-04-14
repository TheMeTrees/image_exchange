import pika
import pdb
import uuid
import os
from ImageExchange.utils import Utils
from .Exceptions.image_not_found_error import ImageNotFoundError


class Producer:
    def __init__(self, exchange_name):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange=exchange_name, exchange_type='direct', durable=True)
        self.exchange_name = exchange_name

    def __del__(self):
        self.connection.close()

    def send_image(self, image_path, directory, routing_key):
        # Need to create an Image object, in order to save on directory, using PIL.save
        try:
            image = Utils.open_image(image_path)
            image_name = str(uuid.uuid4())
            file_path = os.path.join(directory, image_name + ".jpg")
            image.save(file_path)
            self.channel.basic_publish(exchange=self.exchange_name, routing_key=routing_key, body=file_path)
        except FileNotFoundError:
            raise ImageNotFoundError(image_path)
