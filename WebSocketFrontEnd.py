#coding:utf-8
import tornado
import tornado.websocket
import tornado.web
import tornado.httpserver
import tornado.ioloop
import os
import time
import sys

from stormed.connection import Connection
from stormed.channel import Consumer
from stormed.message import Message
from stormed.frame import status
import uuid
import zlib
import getopt

connection_list={}
class RabbitMQServer(tornado.websocket.WebSocketHandler):
    last_act_time=0
    def open(self):
        self.connid=str(uuid.uuid4())
        print self.connid+' connected'
        connection_list[self.connid]=self
        self.last_act_time=time.time()
        self.cip=self.request.remote_ip
    def on_message(self, message):
        msg=Message(body=message,delivery_mode=2,reply_to=mqserver.back_queue)
        msg.headers={"connid":self.connid,'cip':self.cip}
        mqserver.publish(msg)
        self.last_act_time=time.time()
    def on_close(self):
        connection_list.pop(self.connid,'')
        msg=Message(body='{"function":"connection_lost","params":{}}',delivery_mode=2)
        msg.headers={"connid":self.connid,'cip':self.cip}
        mqserver.publish(msg)
    def on_pong(self,data):
        self.last_act_time=time.time()

class RabbitMQ_Queue(object):
    def _start_new_connect(self):
        self.conn=Connection(self.Queue_Server,username=self.Queue_User,password=self.Queue_PassWord
            ,vhost=self.Queue_Path,port=self.Queue_Port, io_loop=tornado.ioloop.IOLoop.instance())
        self.conn.on_disconnect=self.on_queue_disconnect
        self.conn.on_error=self.on_queue_error
        self.conn.connect(self.on_connect)
    def __init__(self,Queue_Server,Queue_User,Queue_PassWord,Queue_Path,Queue_Port=None):
        self.Queue_Server=Queue_Server
        self.Queue_User=Queue_User
        self.Queue_PassWord=Queue_PassWord
        self.Queue_Path=Queue_Path
        self.Queue_Port=Queue_Port
        self.back_queue=str(uuid.uuid4())
        self._start_new_connect()
    def on_connect(self):
        if self.conn.status!=status.OPENED:
            print 'connect rabbitmq fail'
            self.conn.close(self.stop)
        else:
            print 'connect rabbitmq success'
            self.channel = self.conn.channel()
            self.channel.queue_declare('task', durable=True,
                             callback=self.on_queue_creation)
            self.channel.queue_declare(self.back_queue,auto_delete=True,callback=self.on_queue_back_created)
    def on_queue_creation(self,qinfo):
        print "queue %s created"%qinfo.queue
        self.task_queue=qinfo.queue
    def on_queue_back_created(self,qinfo):
        print "back queue %s created"%qinfo.queue
        self.back_queue=qinfo.queue
        consumer = Consumer(self.consume_callback)
        self.channel.consume(qinfo.queue, consumer, no_ack=True)
    def consume_callback(self,msg):
        connid=msg.headers.get("connid",None)
        if connid:
            conn=connection_list.get(connid,None)
            if conn:
                retbody=msg.body
                if msg.headers.get('compression')=='application/x-gzip':
                    retbody=zlib.decompress(retbody)
                conn.write_message(retbody)
                conn.last_act_time=time.time()
    def on_queue_disconnect(self):
        time.sleep(5)
        self._start_new_connect()
    def on_queue_error(self,err):
        print str(err)
        time.sleep(5)
        self._start_new_connect()
    def publish(self,msg):
        self.channel.publish(msg,'',self.task_queue)

CHECK_TIMEOUT=10*60
def RunPingFuncion():
    now=time.time()
    for conn in connection_list.itervalues():
        if now-conn.last_act_time>CHECK_TIMEOUT*2:
            conn.ping(b'0')
    tornado.ioloop.IOLoop.instance().add_timeout(time.time()+CHECK_TIMEOUT,RunPingFuncion)
mqserver=None
def main():
    settings = {
        'template_path': os.path.join(os.path.dirname(__file__), 'templates'),
        'static_path': os.path.join(os.path.dirname(__file__), 'static')
    }
    application = tornado.web.Application([
                                              (r'/ws',RabbitMQServer)
                                              ], **settings)
    http_server = tornado.httpserver.HTTPServer(application,xheaders=True)

    bind_addr='0.0.0.0'
    bind_port=8000
    Queue_User="guest"
    Queue_PassWord="guest"
    Queue_Server='127.0.0.1'
    Queue_Port=5672
    Queue_Path='/websocketserver'
    global mqserver
    opts, args=getopt.getopt(sys.argv[1:],'H:P:h:p:u:w:a:',
                             ['host=','port=','queuehost=','queueport=','queueusr=','queuepsw=','queuepath='])
    for k,v in opts:
        if k in ('-H','--host'):
            bind_addr=v
        elif k in ('-P','--port'):
            bind_port=int(v)
        elif k in ('-h','--queuehost'):
            Queue_Server=v
        elif k in ('-p','--queueport'):
            Queue_Port=int(v)
        elif k in ('-u','--queueusr'):
            Queue_User=v
        elif k in ('-w','--queuepsw'):
            Queue_PassWord=v
        elif k in ('-a','--queuepath'):
            Queue_Path=v
    mqserver=RabbitMQ_Queue(Queue_Server,Queue_User,Queue_PassWord,Queue_Path,Queue_Port)
    http_server.listen(bind_port,bind_addr)
    tornado.ioloop.IOLoop.instance().add_timeout(time.time()+CHECK_TIMEOUT,RunPingFuncion)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == '__main__':
    main()