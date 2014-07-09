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


publish_exchange.publish("body",headers={"message":"you id code:%d"%random.randint(100,100000),
              "uhid":"10c6644d00d6fffbf1eb9f368d7cadacae820a90badc8f625e85ba1a37f5764d","badge":5})
