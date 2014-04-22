__author__ = 'amen'
import time
import random

from kombu import Connection
from kombu.messaging import Producer
from kombu import Exchange


connection = Connection(hostname="192.173.1.213",virtual_host='/websocketserver')
channel = connection.channel()
exchange=Exchange("sys.apn",type='topic',channel=channel,durable=True,delivery_mode=2)
publish_exchange = Producer(channel,exchange,routing_key='msg.debug')

while True:
    publish_exchange.publish("body",headers={"message":"you id code:%d"%random.randint(100,100000),
			      "uhid":"d8009e6c8e074d1bbcb592f321367feaef5674a82fc4cf3b78b066b7c8ad59bd","badge":5})
    time.sleep(5)