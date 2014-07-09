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
import apnsclient
import OpenSSL.crypto
import apnsclient.certificate

class P12Certificate(apnsclient.certificate.BaseCertificate):
    def  load_context(self, cert_string=None, cert_file=None, key_string=None, key_file=None, passphrase=None):
        context = OpenSSL.SSL.Context(OpenSSL.SSL.SSLv3_METHOD)
        p12=OpenSSL.crypto.load_pkcs12(file(cert_file,'rb').read(),passphrase)
        cert =p12.get_certificate()
        context.use_certificate(cert)
        context.use_privatekey(p12.get_privatekey())
        context.check_privatekey()
        return context, cert
    def dump_certificate(self, raw_certificate):
        return OpenSSL.crypto.dump_certificate(OpenSSL.crypto.FILETYPE_PEM, raw_certificate)
    def dump_digest(self, raw_certificate, digest):
        return raw_certificate.digest(digest)


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
con=session.get_connection(apn_connarg[0],certificate=P12Certificate(cert_file=apn_connarg[1],passphrase=apn_connarg[2]))
apnsrv = apnsclient.APNs(con)

try:
    consumer.consume()
    while True:
        connection.drain_events()
    connection.close()
except BaseException,e:
    print traceback.format_exc()
    print e