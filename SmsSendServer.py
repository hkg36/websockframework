from kombu import Connection
from kombu.messaging import Consumer,Producer
from kombu import Exchange, Queue
import importlib
import getopt,sys
import traceback
import json
import urllib
import pycurl
from StringIO import StringIO
from lxml import etree

def RequestWork(params,body):
    jsonobj=json.loads(body)
    content=jsonobj['content']
    phone=jsonobj['phone']
    print 'to phone',phone
    msg = urllib.quote(content.encode('utf-8'))
    curl=pycurl.Curl()
    curl.fp = StringIO()
    curl.setopt(pycurl.URL, ("http://60.191.57.85:8881/sms.aspx?account=771005&password=3F7J4C56&mobile=%s&content=%s&action=send&sendTime=&extno="%
                            (phone,msg)).encode())
    #curl.setopt(pycurl.URL, "http://60.191.57.85:8881/sms.aspx?account=771005&password=3F7J4C56&action=overage")
    curl.setopt(curl.WRITEFUNCTION, curl.fp.write)
    curl.perform()
    curl.fp.seek(0)
    result=curl.fp.read()
    doc=etree.fromstring(result)
    status=doc.xpath('/returnsms/returnstatus/text()')[0]
    remain=doc.xpath('/returnsms/remainpoint/text()')
    if len(remain):
        remain=remain[0]
    print status,remain
def RequestCallBack(body, message):
    headers=message.headers
    try:
        res=RequestWork(headers,body)
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
exchange=Exchange("sys.sms",type='topic',channel=channel,durable=True,delivery_mode=2)
task_queue = Queue(durable=False,routing_key='sms.code',auto_delete=True,exchange=exchange)
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
