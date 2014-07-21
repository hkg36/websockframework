#coding:utf-8
import json
import os
import ssl
import time
import sys
import uuid
import zlib
import getopt
import importlib

import tornado
import tornado.websocket
import tornado.web
import tornado.httpserver
import tornado.ioloop
from stormed.connection import Connection
from stormed.channel import Consumer
from stormed.message import Message
from stormed.frame import status
from tools.json_tools import DefJsonEncoder
from tools.session import GenSession
import hashlib


connection_client=None

private_code='JdYQIaDBRrdVKzIWgh8oGc9nURaFCCYI9U3y9LUnt0eD85a8sGQcY8Sq0k4S92cnYgrnObD4nELHPDY3n6Ni74o2bnlMFNjKmjjakCC8Q3qOTCri9YS9CtyKm6p9Umex7Dl6RKAvtygpNj35Y4MUowMOvulR5amRjeMw7ZVQV56PML5cJTJVpk9pnH6QtfrRzqQTijST'

class RabbitMQServer(tornado.websocket.WebSocketHandler):
    def open(self):
        self.ccode=GenSession(20)
        self.write_message(DefJsonEncoder.encode({"ccode":self.ccode}))

    def on_message(self, message):
        global private_code
        try:
            data=json.loads(message)
        except Exception,e:
            print str(e)
            return
        if "check" in data:
            check=data['check']
            allstr=self.ccode+private_code
            if isinstance(allstr,unicode):
                allstr=allstr.encode('utf-8')
            if check==hashlib.sha256(allstr).hexdigest():
                global connection_client
                if connection_client!=self:
                    if connection_client:
                        connection_client.close()
                    connection_client=self
                print "pass"
            else:
                self.close()
    def on_close(self):
        global connection_client
        if connection_client:
            connection_client.close()
        connection_client=None
    def on_pong(self,data):
        pass

phone_pre=set(("134","135","136","137","138","139","147","150","151","152","157","158","159","182","183","184","187","188"))
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
        self._start_new_connect()
    def on_connect(self):
        if self.conn.status!=status.OPENED:
            print 'connect rabbitmq fail'
            self.conn.close(self.stop)
        else:
            print 'connect rabbitmq success'
            self.channel = self.conn.channel()
            self.channel.queue_declare(auto_delete=True,callback=self.on_queue_back_created,durable=False)
    def on_queue_back_created(self,qinfo):
        print "back queue %s created"%qinfo.queue
        self.back_queue=qinfo.queue
        self.channel.queue_bind(self.back_queue,"sys.sms",routing_key='sms.code',callback=self.on_queue_binded)
        consumer = Consumer(self.consume_callback)
        self.channel.consume(self.back_queue, consumer, no_ack=True)
    def on_queue_binded(self):
        print "queue binded"

    def consume_callback(self,msg):
        compressed=msg.headers.get('compression')=='application/x-gzip'
        if compressed:
            retbody=zlib.decompress(msg.body)
        else:
            retbody=msg.body
        global phone_pre
        js_data=json.loads(retbody)
        #if js_data['phone'][0:3] in phone_pre:
        if True:
            global connection_client
            if connection_client:
                connection_client.write_message(retbody)
    def on_queue_disconnect(self):
        time.sleep(5)
        self._start_new_connect()
    def on_queue_error(self,err):
        time.sleep(5)
        self._start_new_connect()
    def publish(self,msg):
        self.channel.publish(msg,'',self.task_queue)

mqserver=None
def main():
    settings = {
        'template_path': os.path.join(os.path.dirname(__file__), 'templates'),
        'static_path': os.path.join(os.path.dirname(__file__), 'static')
    }
    application = tornado.web.Application([
                                              (r'/ws',RabbitMQServer)
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

    https_server = tornado.httpserver.HTTPServer(application,xheaders=True,
                  ssl_options = {
    "certfile": os.path.join("configs/ssl.crt"),
    "keyfile": os.path.join("configs/domain.key")
    })
    https_server.listen(configs.bind_port+2,configs.bind_addr)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == '__main__':
    main()