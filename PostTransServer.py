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
import dbconfig
from tools.helper import AutoFitJson


def RequestWork(params,body,reply_queue):
    post=json.loads(body)
    gid=post['gid']
    uid=post['uid']
    uids=set()
    with dbconfig.Session() as session:
        group=session.query(Group).filter(Group.gid==gid).first()
        if group is None:
            return

        gwus=session.query(GroupMember).filter(GroupMember.gid==gid).all()
        #gwus=session.query(GroupWatchUpdate).filter(GroupWatchUpdate.gid==gid).all()
        for gwu in gwus:
            uids.add(gwu.uid)

        if group.only_member_watch==0:
            fds=session.query(FriendList).filter(FriendList.friendid==uid).all()
            for fd in fds:
                uids.add(fd.uid)
        allconn=session.query(ConnectionInfo).filter(ConnectionInfo.uid.in_(list(uids))).all()
        to_push=json.dumps({"push":True,
                                    "type":"newpost",
                                    "data":{
                                        "post":post
                                    }
                                },ensure_ascii=False,cls=AutoFitJson,separators=(',', ':'))
        online_uids=set()
        for conn in allconn:
            online_uids.add(conn.uid)
            QueueWork.producer.publish(body=to_push,delivery_mode=2,headers={"connid":conn.connection_id},
                                      routing_key=conn.queue_id,
                                      compression='gzip')
        offline_uids=list(uids-online_uids)
        print "offline_uids",offline_uids
        if len(offline_uids)>0:
            iosdevices=session.query(IOSDevice).filter(IOSDevice.uid.in_(offline_uids)).all()
            print 'ios device:',len(iosdevices)
            fromuser=session.query(User).filter(User.uid==uid).first()
            push_word=u"%s在%s说:%s"%(fromuser.nick,group.group_name,post['content'])
            print push_word
            for iosdev in iosdevices:
                if iosdev.is_debug:
                    publish_debug_exchange.publish("body",headers={"message":push_word,
                      "uhid":iosdev.device_token,"badge":iosdev.badge+1})
                else:
                    publish_release_exchange.publish("body",headers={"message":push_word,
                      "uhid":iosdev.device_token,"badge":iosdev.badge+1})
                iosdev.badge=iosdev.badge+1
                iosdev=session.merge(iosdev)
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
                    configs.Queue_User,configs.Queue_PassWord,'sys.post_to_notify')
    exchange=Exchange("sys.apn",type='topic',channel=QueueWork.channel,durable=True,delivery_mode=2)
    publish_debug_exchange = Producer(QueueWork.channel,exchange,routing_key='msg.debug')
    publish_release_exchange = Producer(QueueWork.channel,exchange,routing_key='msg.release')
    QueueWork.run()