#coding:utf-8
__author__ = 'amen'
import traceback
import codecs

from kombu import Connection, Exchange
from kombu.messaging import Consumer,Producer
from kombu import Queue
import kombu.serialization
import json


def word_decode(t, coding):
    return codecs.decode(t,coding,'ignore')
kombu.serialization._decode=word_decode

connection=None
channel=None
producer=None
task_queue=None
consumer=None
WorkFunction=None
def init(host,port,virtual_host,usr,psw,queue_name,exchange_name=None):
    global connection,channel,producer,task_queue,consumer
    connection = Connection(hostname=host,port=port,userid=usr,password=psw,virtual_host=virtual_host)
    channel = connection.channel()
    producer=Producer(channel)

    if exchange_name:
        exchange=Exchange(exchange_name,'topic',channel,durable=True,delivery_mode=2)
        task_queue = Queue(queue_name,routing_key=queue_name,durable=True,exchange=exchange)
    else:
        task_queue = Queue(queue_name,durable=True)
    consumer = Consumer(channel,task_queue,no_ack=False)
    consumer.qos(prefetch_count=1)
    consumer.register_callback(RequestCallBack)
def run():
    global connection,channel,producer,task_queue,consumer
    try:
        consumer.consume()
        try:
            while True:
                connection.drain_events()
        except Exception,e:
            print e
        connection.close()
    except BaseException,e:
        print traceback.format_exc()
        print e

def RequestCallBack(body, message):
    properties=message.properties
    headers=message.headers
    replyheader=None
    replybody=None
    try:
        res=WorkFunction(headers,body,properties.get('reply_to'))
        if res is None:
            message.ack()
            return
        replyheader,replybody=res
    except Exception,e:
        replybody = traceback.format_exc()
        replyheader={'error':str(e)}
    if 'reply_to' in properties:
        if replyheader.get('zip'):
            producer.publish(body=replybody,delivery_mode=2,headers=replyheader,
                                  routing_key=properties['reply_to'],
                                  correlation_id=properties.get('correlation_id'),
                                  content_type='application/data',
                                  content_encoding='binary')
        else:
            producer.publish(body=replybody,delivery_mode=2,headers=replyheader,
                                  routing_key=properties['reply_to'],
                                  correlation_id=properties.get('correlation_id'),
                                  compression='gzip')
    else:
        print json.dumps(replyheader),replybody
    message.ack()
