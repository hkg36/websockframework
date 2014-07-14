#coding:utf-8
import importlib
import getopt
import sys
import traceback
import json
import urllib
import pycurl
from StringIO import StringIO

from kombu import Connection
from kombu.messaging import Consumer,Producer
from kombu import Exchange, Queue
from lxml import etree
import uuid
import time

def RequestCallBack(body, message):
    headers=message.headers
    try:
        uid=int(headers['uid'])
        connid=uuid.UUID(hex=headers['connid'])
        ip=headers['cip']
        suuid=uuid.UUID(hex=headers['suuid'])
        stime=time.mktime(time.strptime(headers['stime'],"%Y-%m-%d %H:%M:%S"))
        front_back=message.properties['reply_to']
        print uid,connid,ip,suuid,stime,front_back

        #切断连接
        #producer.publish('1',headers={'close_connect':'1','connid':connid.hex},exchange='front_end',routing_key=front_back)
    except Exception,e:
        print str(e)
    message.ack()

config_model='configs.frontend'
opts, args=getopt.getopt(sys.argv[1:],'c:',
                         ['config='])
for k,v in opts:
    if k in ('-c','--config'):
        config_model=v
try:
    configs=importlib.import_module(config_model)
except Exception,e:
    print str(e)
    exit(0)

connection = Connection(hostname=configs.Queue_Server,port=configs.Queue_Port,
                        userid=configs.Queue_User,password=configs.Queue_PassWord,virtual_host=configs.Queue_Path)
channel = connection.channel()
producer=Producer(channel)
exchange=Exchange("front_end",type='topic',channel=channel,durable=True,delivery_mode=2)
task_queue = Queue(durable=False,routing_key='task.front',auto_delete=True,exchange=exchange)
consumer = Consumer(channel,task_queue,no_ack=False)
consumer.qos(prefetch_count=1)
consumer.register_callback(RequestCallBack)

try:
    consumer.consume()
    while True:
        connection.drain_events()
    connection.close()
except BaseException,e:
    print traceback.format_exc()
    print e
