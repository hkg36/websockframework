#coding:utf-8
from kombu import Exchange, Producer

from datamodel.ios import IOSDevice
from datamodel.user import User


__author__ = 'amen'
import QueueWork
import getopt
import importlib
import sys
from datamodel.connection_info import ConnectionInfo
import dbconfig
import json


def RequestWork(params,body,reply_queue):
    post=json.loads(body)
    toid=post['toid']
    with dbconfig.Session() as session:
        conn=session.query(ConnectionInfo).filter(ConnectionInfo.uid==toid).first()
        if conn:
            to_push=json.dumps({"push":True,
                                        "type":"newmsg",
                                        "data":{
                                            "message":post
                                        }
                                    },ensure_ascii=False)
            QueueWork.producer.publish(body=to_push,delivery_mode=2,headers={"connid":conn.connection_id},
                                          routing_key=conn.queue_id,
                                          compression='gzip')
        else:
            iosdev=session.query(IOSDevice).filter(IOSDevice.uid==toid).first()
            if iosdev:
                user=session.query(User).filter(User.uid==post['fromid']).first()
                allword=None
                if post.get('content',None):
                    content=post['content']
                    if content.startswith('sticker_12636'):
                        allword=u"%s发了一个表情"%(user.nick)
                    else:
                        allword=u"%s:%s"%(user.nick,post['content'])
                elif post.get('picture',None):
                    allword=u"%s发了一张图片"%(user.nick)
                elif post.get('video',None):
                    allword=u"%s发了一段视频"%(user.nick)
                elif post.get('voice',None):
                    allword=u"%s发了一段音频"%(user.nick)
                elif post.get('lat',None):
                    allword=u"%s发了一个位置"%(user.nick)
                if allword:
                    if iosdev.is_debug:
                        publish_debug_exchange.publish("body",headers={"message":allword,
                          "uhid":iosdev.device_token})
                    else:
                        publish_release_exchange.publish("body",headers={"message":allword,
                          "uhid":iosdev.device_token})
exchange=None
publish_debug_exchange = None
publish_release_exchange = None
if __name__ == '__main__':
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
    QueueWork.WorkFunction=RequestWork
    QueueWork.init(configs.Queue_Server,configs.Queue_Port,configs.Queue_Path,
                    configs.Queue_User,configs.Queue_PassWord,'sys.message_to_notify')
    exchange=Exchange("sys.apn",type='topic',channel=QueueWork.channel,durable=True,delivery_mode=2)
    publish_debug_exchange = Producer(QueueWork.channel,exchange,routing_key='msg.debug')
    publish_release_exchange = Producer(QueueWork.channel,exchange,routing_key='msg.release')
    QueueWork.run()