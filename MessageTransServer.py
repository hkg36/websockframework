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
from datamodel.group import GroupWatchUpdate
from datamodel.friendlist import FriendList
import dbconfig
import anyjson
import zlib

def RequestWork(params,body,reply_queue):
    post=anyjson.loads(body)
    toid=post['toid']
    with dbconfig.Session() as session:
        conn=session.query(ConnectionInfo).filter(ConnectionInfo.uid==toid).first()
        if conn:
            to_push=anyjson.dumps({"push":True,
                                        "type":"newmsg",
                                        "data":{
                                            "message":post
                                        }
                                    })
            QueueWork.producer.publish(body=to_push,delivery_mode=2,headers={"connid":conn.connection_id},
                                          routing_key=conn.queue_id,
                                          compression='gzip')
        else:
            iosdev=session.query(IOSDevice).filter(IOSDevice.uid==toid).first()
            if iosdev:
                user=session.query(User).filter(User.uid==post['fromid']).first()
                allword=None
                if 'content' in post:
                    allword=u"%s:%s"%(user.nick,post['content'])
                else:
                    allword=u"%s发了个图"%(user.nick)
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