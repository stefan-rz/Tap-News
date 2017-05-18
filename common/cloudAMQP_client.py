import json
import logging
import os
import pika
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'config'))
from applogconfig import app_log

class CloudAMQPClient:
    def __init__(self, cloud_amqp_url, queue_name):
        self.cloud_amqp_url = cloud_amqp_url
        self.queue_name = queue_name
        self.params = pika.URLParameters(cloud_amqp_url)
        self.params.socket_timeout = 3
        self.connection = pika.BlockingConnection(self.params)
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=queue_name)

    # send a message
    def sendMessage(self, message):
        self.channel.basic_publish(exchange='',
                                   routing_key=self.queue_name,
                                   body=json.dumps(message))
        app_log.info("[X] Sent message to %s: %s" % (self.queue_name, message))
        return

    # get a message
    def getMessage(self):
        method_frame, header_frame, body = self.channel.basic_get(self.queue_name)
        if method_frame is not None:
            app_log.info("[O] Received message from %s: %s" % (self.queue_name, body))
            self.channel.basic_ack(method_frame.delivery_tag)
            return json.loads(body)
        else:
            app_log.info("No message returned")
            return None

    # sleep
    def sleep(self, seconds):
        self.connection.sleep(seconds)

