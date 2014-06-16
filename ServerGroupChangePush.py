#coding:utf-8
from kombu import Exchange, Producer
import getopt
import importlib
import sys
import json

import QueueWork
from datamodel.connection_info import ConnectionInfo
from datamodel.group import Group
from datamodel.group_member import GroupMember
from datamodel.ios import IOSDevice
from datamodel.user import User
from datamodel.user_circle import UserCircle, CircleDef
import dbconfig
from tools.helper import AutoFitJson, DefJsonEncoder
from tools.with_cache import GetUserInfo


def RequestWork(params,body,reply_queue):
    post=json.loads(body)
    gid=post['gid']
    with dbconfig.Session() as session:
        userlist=session.query(GroupMember).filter(GroupMember.gid==gid).all()
        uids=set([one.uid for one in userlist])

        allconn=session.query(ConnectionInfo).filter(ConnectionInfo.uid.in_(list(uids))).all()
        to_push=DefJsonEncoder.encode({"push":True,
                                    "type":params['type'],
                                    "data":post
                                })
        online_uids=set()
        queue_group={}
        for conn in allconn:
            online_uids.add(conn.uid)
            connids=queue_group.get(conn.queue_id,None)
            if connids is None:
                connids=[]
                queue_group[conn.queue_id]=connids
            connids.append(conn.connection_id)
        for conn_id in queue_group:
            QueueWork.producer.publish(body=to_push,delivery_mode=2,headers={"connid":"$".join(queue_group[conn_id])},
                                          routing_key=conn_id,
                                          compression='gzip')
        offline_uids=list(uids-online_uids)
        #print "offline_uids",offline_uids
        if len(offline_uids)>0:
            iosdevices=session.query(IOSDevice).filter(IOSDevice.uid.in_(offline_uids)).all()
            #print 'ios device:',len(iosdevices)
            group_info=session.query(Group).filter(Group.gid==gid).first()
            user_info=GetUserInfo(post['uid'])
            push_word=None
            if params['type']=="group.newpost":
                push_word=u"%s在%s"%(user_info['user']['nick'],group_info.group_name)
                if 'content' in post:
                    if len(post['content'])>20:
                        push_word+=u"说 %s..."%(post['content'][0:20])
                    else:
                        push_word+=u"说 %s"%(post['content'])
                elif 'pictures' in post:
                    push_word+=u"发了几张图片"
            #print push_word
            if push_word:
                for iosdev in iosdevices:
                    if iosdev.is_debug:
                        publish_debug_exchange.publish("body",headers={"message":push_word,
                          "uhid":iosdev.device_token,"badge":iosdev.badge+1})
                    else:
                        publish_release_exchange.publish("body",headers={"message":push_word,
                          "uhid":iosdev.device_token,"badge":iosdev.badge+1})
                session.query(IOSDevice).filter(IOSDevice.uid.in_(offline_uids)).update({IOSDevice.badge:IOSDevice.badge+1},False)
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
                    configs.Queue_User,configs.Queue_PassWord,'group.change')
    exchange=Exchange("sys.apn",type='topic',channel=QueueWork.channel,durable=True,delivery_mode=2)
    publish_debug_exchange = Producer(QueueWork.channel,exchange,routing_key='msg.debug')
    publish_release_exchange = Producer(QueueWork.channel,exchange,routing_key='msg.release')
    QueueWork.run()
