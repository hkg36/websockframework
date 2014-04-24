#coding:utf-8
import time
import random
import json

from kombu import Connection
from kombu.messaging import Producer
from kombu import Exchange


connection = Connection(hostname="192.168.10.201",virtual_host='/websocketserver')
channel = connection.channel()
publish_exchange = Producer(channel,routing_key='sys.sendweixin')


publish_exchange.publish(json.dumps({
    'weixin_users':['o8Td4joS0bB4fMekczcIoH1id7Qc'],
    'body':{
        "msgtype":"text",
        "text":
        {
             "content":"完整测试"
        }
    }
}))

