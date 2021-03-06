#coding:utf-8
import os
import ssl
import time
import sys
import uuid
import zlib
import getopt
import importlib
import msgpack
import json
import base64

import tornado
import tornado.websocket
import tornado.web
import tornado.httpserver
import tornado.ioloop
from stormed.connection import Connection
from stormed.channel import Consumer
from stormed.message import Message
from stormed.frame import status
from tools.crypt_session import DecodeCryptSession
from tools.json_tools import  DefJsonEncoder

connection_list={}
class RabbitMQServer(tornado.websocket.WebSocketHandler):
    def check_origin(self, origin):
        return True
    last_act_time=0
    def open(self):
        self.usezlib=int(self.get_argument('usezlib',0))

        sessionid=self.get_argument('sessionid',None)
        cdata=self.get_argument('cdata',None)
        self.userdata=None
        if sessionid:
            self.userdata=DecodeCryptSession(sessionid)
            if self.userdata:
                self.userdata['uid']=str(self.userdata['uid'])
        if sessionid and self.userdata is None:
            self.close()
            return

        self.connid=uuid.uuid4().get_hex()
        print self.connid+' connected'
        connection_list[self.connid]=self
        self.last_act_time=time.time()
        self.cip=self.request.remote_ip

        if self.userdata:
            msgbody=DefJsonEncoder.encode(
                {
                    "func":"session.start2",
                    "parm":{
                        "sessionid":None,
                    },
                    "cdata":cdata
                }
            )
            msg=Message(body=msgbody,delivery_mode=2,reply_to=mqserver.back_queue)
            msg.headers={"connid":self.connid,'cip':self.cip,"uid":self.userdata['uid'],
                         'stime':time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(self.userdata.get('time'))),'suuid':self.userdata.get('uuid').hex}
            mqserver.publish(msg)
    def on_message(self, message):
        try:
            if self.usezlib:
                message=zlib.decompress(message)
        except Exception,e:
            pass
        msg=Message(body=message,delivery_mode=2,reply_to=mqserver.back_queue)
        msg.headers={"connid":self.connid,'cip':self.cip}
        if self.userdata:
            msg.headers['uid']=self.userdata['uid']
        mqserver.publish(msg)
        self.last_act_time=time.time()
    def on_close(self):
        print "%s closed"%self.connid
        connection_list.pop(self.connid,'')
        msg=Message(body='{"func":"connection_lost","parm":{}}',delivery_mode=2)
        msg.headers={"connid":self.connid,'cip':self.cip}
        if self.userdata:
            msg.headers['uid']=self.userdata['uid']
        mqserver.publish(msg)
    def on_pong(self,data):
        self.last_act_time=time.time()
    def SendData(self,data,compressed):
        if compressed and not self.usezlib:
            data=zlib.decompress(data)
        elif not compressed and self.usezlib:
            data=zlib.compress(data)
        self.write_message(data,binary=self.usezlib)
        self.last_act_time=time.time()

class MessagePackServer(RabbitMQServer):
    def on_message(self, message):
        message=DefJsonEncoder.encode(msgpack.unpackb(message))
        msg=Message(body=message,delivery_mode=2,reply_to=mqserver.back_queue)
        msg.headers={"connid":self.connid,'cip':self.cip}
        mqserver.publish(msg)
        self.last_act_time=time.time()
    def SendData(self,data,compressed):
        if compressed:
            data=zlib.decompress(data)
        try:
            data=json.loads(data)
        except Exception,e:
            self.write_message(data)
            return
        data=msgpack.packb(data)
        self.write_message(data,binary=True)
        self.last_act_time=time.time()

start_notified=False
class RabbitMQ_Queue(object):
    def _start_new_connect(self):
        self.conn=Connection(self.Queue_Server,username=self.Queue_User,password=self.Queue_PassWord
            ,vhost=self.Queue_Path,port=self.Queue_Port, io_loop=tornado.ioloop.IOLoop.instance())
        self.conn.on_disconnect=self.on_queue_disconnect
        self.conn.on_error=self.on_queue_error
        self.conn.connect(self.on_connect)
    def __init__(self,Queue_Server,Queue_User,Queue_PassWord,Queue_Path,BackQueueName,Queue_Port=None):
        self.Queue_Server=Queue_Server
        self.Queue_User=Queue_User
        self.Queue_PassWord=Queue_PassWord
        self.Queue_Path=Queue_Path
        self.Queue_Port=Queue_Port
        self.back_queue="WSBack-%s.resback"%BackQueueName
        self._start_new_connect()
    def on_connect(self):
        if self.conn.status!=status.OPENED:
            print 'connect rabbitmq fail'
            self.conn.close(self.stop)
        else:
            print 'connect rabbitmq success'
            self.channel = self.conn.channel()
            self.channel.qos(prefetch_count=1)
            self.channel.exchange_declare('front_end',type='topic',durable=True,callback=self.on_exchange_declare)

    def on_exchange_declare(self):
        self.channel.queue_declare(self.back_queue,auto_delete=True,callback=self.on_queue_back_created,durable=False)

        print "exchange %s created"%'front_end'
        #self.task_queue=qinfo.queue

        global start_notified
        if start_notified==False:
            start_notified=True
            msg=Message(body='{"func":"front_end_restart","parm":{}}',delivery_mode=2,reply_to=self.back_queue)
            self.publish(msg)

    def on_queue_back_created(self,qinfo):
        print "back queue %s created"%qinfo.queue
        self.back_queue=qinfo.queue
        self.channel.queue_bind(self.back_queue,'front_end',self.back_queue,self.on_backqueue_bind)
        consumer = Consumer(self.consume_callback)
        self.channel.consume(qinfo.queue, consumer, no_ack=True)
    def on_backqueue_bind(self):
        print "back queue %s bind"%self.back_queue
    def consume_callback(self,msg):
        connid=msg.headers.get("connid",None)
        if connid:
            connids=connid.split("$")
            for oneid in connids:
                conn=connection_list.get(oneid,None)
                if conn:
                    if int(msg.headers.get("close_connect",0)):
                        connection_list.pop(conn.connid,'')
                        conn.close()
                        conn.on_close()
                        continue
                    compressed=msg.headers.get('compression')=='application/x-gzip'
                    conn.SendData(msg.body,compressed)
    def on_queue_disconnect(self):
        time.sleep(5)
        self._start_new_connect()
    def on_queue_error(self,err):
        time.sleep(5)
        self._start_new_connect()
    def publish(self,msg):
        self.channel.publish(msg,'front_end','task.front')

CHECK_TIMEOUT=5*60
def RunPingFuncion():
    now=time.time()
    for key in connection_list.keys():
        conn=connection_list[key]
        if now-conn.last_act_time>CHECK_TIMEOUT*2:
            connection_list.pop(conn.connid,'')
            conn.close()
            conn.on_close()
        elif now-conn.last_act_time>CHECK_TIMEOUT:
            conn.ping(b'')
    tornado.ioloop.IOLoop.instance().add_timeout(time.time()+CHECK_TIMEOUT,RunPingFuncion)
mqserver=None

class GetConnectionList(tornado.web.RequestHandler):
    def get(self):
        connlist=[]
        for connid in connection_list:
            conn=connection_list[connid]
            if isinstance(conn,RabbitMQServer) and conn.userdata:
                data={'connid':connid,'uuid':(conn.userdata['uuid']),
                      'uid':conn.userdata['uid'],'time':conn.userdata['time']}
                connlist.append(data)
        self.write(str(connlist))
def main():
    settings = {
        'template_path': os.path.join(os.path.dirname(__file__), 'templates'),
        'static_path': os.path.join(os.path.dirname(__file__), 'static')
    }
    application = tornado.web.Application([
                                              (r'/ws',RabbitMQServer),
                                              (r'/msgpack',MessagePackServer),
                                              (r'/tools/getconn',GetConnectionList),
                                              ], **settings)


    config_model='configs.frontend'
    global mqserver
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
    mqserver=RabbitMQ_Queue(configs.Queue_Server,configs.Queue_User,
                            configs.Queue_PassWord,configs.Queue_Path,configs.front_name,configs.Queue_Port)

    http_server = tornado.httpserver.HTTPServer(application,xheaders=True)
    http_server.listen(configs.bind_port,configs.bind_addr)
    https_server = tornado.httpserver.HTTPServer(application,xheaders=True,
                  ssl_options = {
    "certfile": os.path.join("configs/ssl.crt"),
    "keyfile": os.path.join("configs/domain.key")
    })
    https_server.listen(configs.bind_port+1,configs.bind_addr)
    tornado.ioloop.IOLoop.instance().add_timeout(time.time()+CHECK_TIMEOUT,RunPingFuncion)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == '__main__':
    main()