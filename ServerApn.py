#coding:utf-8
import importlib
import getopt
import sys
import traceback

from kombu import Connection
from kombu.messaging import Consumer,Producer
from kombu import Exchange, Queue
import apnsclient
import tools.APN_Tools

def RequestWork(params,body):
    print params
    message=params['message']
    uhid=params['uhid']
    badge=params.get('badge',None)
    apnmsg=apnsclient.Message([uhid], alert=message, badge=badge)
    apnsrv.send(apnmsg)

def RequestCallBack(body, message):
    headers=message.headers
    try:
        res=RequestWork(headers,body)
    except Exception,e:
        print str(e)
    message.ack()

config_model='configs.frontend'
opts, args=getopt.getopt(sys.argv[1:],'c:d:',
                         ['config=','debug='])
debug_mod=1
for k,v in opts:
    if k in ('-c','--config'):
        config_model=v
    if k in ('-d','--debug'):
        debug_mod=int(v)
try:
    configs=importlib.import_module(config_model)
except Exception,e:
    print str(e)
    exit(0)

if debug_mod:
    apn_connarg=['push_sandbox','configs/laixin_debug.p12','Laixin123']
else:
    apn_connarg=['push_production','configs/laixin_release.p12','Laixin123']

connection = Connection(hostname=configs.Queue_Server,port=configs.Queue_Port,
                        userid=configs.Queue_User,password=configs.Queue_PassWord,virtual_host=configs.Queue_Path)
channel = connection.channel()
producer=Producer(channel)
exchange=Exchange("sys.apn",type='topic',channel=channel,durable=True,delivery_mode=2)
task_queue = Queue(durable=False,routing_key='msg.debug' if debug_mod else 'msg.release',auto_delete=True,exchange=exchange)
consumer = Consumer(channel,task_queue,no_ack=False)
consumer.qos(prefetch_count=1)
consumer.register_callback(RequestCallBack)

session=apnsclient.Session()
con=session.get_connection(apn_connarg[0],certificate=tools.APN_Tools.P12Certificate(cert_file=apn_connarg[1],passphrase=apn_connarg[2]))
apnsrv = apnsclient.APNs(con)

try:
    consumer.consume()
    while True:
        connection.drain_events()
    connection.close()
except BaseException,e:
    print traceback.format_exc()
    print e