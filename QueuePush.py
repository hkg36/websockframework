#coding:utf-8
import sys

from kombu import Connection
from kombu.messaging import Consumer,Producer
from kombu import Exchange, Queue

class QueuePush(object):
    def __init__(self,Queue_Server,Queue_Port,Queue_User,Queue_PassWord,Queue_Path):
        self.usr=Queue_User
        self.psw=Queue_PassWord
        self.server=Queue_Server
        self.port=Queue_Port
        self.path=Queue_Path
        self.connection=None
    def Push(self,queueid,connectid,body):
        self.rawPush(queueid,{'connid':connectid},body)
    def Close(self,queueid,connectid):
        self.rawPush(queueid,{'connid':connectid,'close_connect':'1'},'close')
    def rawPush(self,routing_key,headers,body):
        if self.connection is None or self.connection.connected==False:
            self.connection = Connection(hostname=self.server,port=self.port,userid=self.usr,password=self.psw,virtual_host=self.path)
            self.channel = self.connection.channel()
            self.producer=Producer(self.channel)
        self.producer.publish(body=body,delivery_mode=2,headers=headers,
                              routing_key=routing_key,retry=True)
if __name__ == '__main__':
    Queue_User="guest"
    Queue_PassWord="guest"
    Queue_Server='127.0.0.1'
    Queue_Port=None
    Queue_Path='/websocketserver'

    pusher=QueuePush(Queue_Server,Queue_Port,Queue_User,Queue_PassWord,Queue_Path)
    queueid=None
    connid=None
    while True:
        vin=raw_input('need queueid(empty for use lastone):')
        if vin:
            queueid=vin
        vin=raw_input('need connid(empty for use lastone):')
        if vin:
            connid=vin
        vin=raw_input('content to send:')
        if not queueid or not connid:
            print 'queueid or connid error'
            continue
        if not vin:
            print 'nothing to send'
            continue
        if vin=='close':
            pusher.Close(queueid,connid)
        else:
            pusher.Push(queueid,connid,vin)
