import json

__author__ = 'amen'
import time
import random

from kombu import Connection
from kombu.messaging import Producer
from kombu import Exchange


connection = Connection(hostname="192.173.1.213",virtual_host='/websocketserver')
channel = connection.channel()
exchange=Exchange("sys.sms",type='topic',channel=channel,durable=True,delivery_mode=2)
publish_exchange = Producer(channel,exchange,routing_key='sms.code')

while True:
    publish_exchange.publish(json.dumps({'content':"code %d"%random.randint(100,500),'phone':"15034445667"}))
    time.sleep(5)
