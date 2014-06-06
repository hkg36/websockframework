#coding:utf-8

import json

from kombu import Connection
from kombu.messaging import Producer
from kombu import Exchange


class QueuePush(object):
    def __init__(self,Queue_Server,Queue_Port,Queue_User,Queue_PassWord,Queue_Path):
        self.usr=Queue_User
        self.psw=Queue_PassWord
        self.server=Queue_Server
        self.port=Queue_Port
        self.path=Queue_Path
        self.connection=None
        self.smsExchange=None
    def _InitConnect(self):
        if self.connection is None or self.connection.connected==False:
            self.connection = Connection(hostname=self.server,port=self.port,userid=self.usr,password=self.psw,virtual_host=self.path)
            self.channel = self.connection.channel()
            self.producer=Producer(self.channel)
            self.smsExchange=Exchange("sys.sms",type='topic',channel=self.channel,durable=True,delivery_mode=2)
            self.smsCodeProduce=Producer(self.channel,self.smsExchange,routing_key='sms.code')
    def Push(self,queueid,connectid,body):
        self.rawPush(queueid,{'connid':connectid},body)
    def Close(self,queueid,connectid):
        self.rawPush(queueid,{'connid':connectid,'close_connect':'1'},'close')
    def rawPush(self,routing_key,headers,body,exchange=None):
        self._InitConnect()
        self.producer.publish(body=body,delivery_mode=2,headers=headers,
                              routing_key=routing_key,retry=True,compression='gzip',exchange=exchange)
    def sendCode(self,phone,code):
        self._InitConnect()
        json_str=json.dumps({'phone':str(phone),"content":u"您的来信验证码为:%s，请在5分钟内输入完成验证."%str(code)},ensure_ascii=False)
        self.smsCodeProduce.publish(body=json_str,retry=True,compression='gzip')
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
