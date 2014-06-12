#coding:utf-8
from kombu import Exchange, Producer
import getopt
import importlib
import sys
import json

import QueueWork
from datamodel.connection_info import ConnectionInfo
from datamodel.friendlist import FriendList
from datamodel.group import Group
from datamodel.group_member import GroupMember
from datamodel.ios import IOSDevice
from datamodel.user import User
from datamodel.user_circle import UserCircle, CircleDef
import dbconfig
from tools.helper import AutoFitJson, DefJsonEncoder


def RequestWork(params,body,reply_queue):
    post=json.loads(body)
    touid=params['uid']
    with dbconfig.Session() as session:
        to_push=DefJsonEncoder.encode({"push":True,
                                    "type":params['type'],
                                    "data":post
                                })
        conn=session.query(ConnectionInfo).filter(ConnectionInfo.uid==touid).first()
        if conn:
            QueueWork.producer.publish(body=to_push,delivery_mode=2,headers={"connid":conn.connection_id},
                                          routing_key=conn.queue_id,
                                          compression='gzip')
        else:
            iosdev=session.query(IOSDevice).filter(IOSDevice.uid==touid).first()
            #print 'ios device:',len(iosdevices)
            push_word=None
            #print push_word
            if push_word:
                if iosdev.is_debug:
                    publish_debug_exchange.publish("body",headers={"message":push_word,
                      "uhid":iosdev.device_token,"badge":iosdev.badge+1})
                else:
                    publish_release_exchange.publish("body",headers={"message":push_word,
                      "uhid":iosdev.device_token,"badge":iosdev.badge+1})
                session.query(IOSDevice).filter(IOSDevice.uid==touid).update({IOSDevice.badge:IOSDevice.badge+1},False)
                session.commit()

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
                    configs.Queue_User,configs.Queue_PassWord,'sys.push_to_user')
    exchange=Exchange("sys.apn",type='topic',channel=QueueWork.channel,durable=True,delivery_mode=2)
    publish_debug_exchange = Producer(QueueWork.channel,exchange,routing_key='msg.debug')
    publish_release_exchange = Producer(QueueWork.channel,exchange,routing_key='msg.release')
    QueueWork.run()
