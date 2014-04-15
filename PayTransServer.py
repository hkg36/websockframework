#coding:utf-8
from kombu import Exchange, Producer
from sqlalchemy import and_, or_

from datamodel.ios import IOSDevice
from datamodel.user import User
from tools.helper import AutoFitJson


__author__ = 'amen'
import QueueWork
import getopt
import importlib
import sys
from datamodel.connection_info import ConnectionInfo
import dbconfig
import json
import tools.weixin as weixin

def RequestWork(params,body,reply_queue):
    post=json.loads(body)
    toids={post['uid'],post['recommend_uid']}
    with dbconfig.Session() as session:
        conns=session.query(ConnectionInfo).filter(ConnectionInfo.uid.in_(list(toids))).all()
        if len(conns)>0:
            to_push=json.dumps({"push":True,
                                        "type":"paylog",
                                        "data":{
                                            "log":post
                                        }
                                    },ensure_ascii=False,cls=AutoFitJson,separators=(',', ':'))
            for conn in conns:
                toids.remove(conn.uid)
                QueueWork.producer.publish(body=to_push,delivery_mode=2,headers={"connid":conn.connection_id},
                                              routing_key=conn.queue_id,
                                              compression='gzip')

        iosdevs=session.query(IOSDevice).filter(IOSDevice.uid.in_(list(toids))).all()
        if len(iosdevs)>0:
            allword=u"订单[%s] %.2f元,已支付成功,详情可查看订单历史"%(post['productname'],float(post['amount'])/100)
            for iosdev in iosdevs:
                if iosdev.is_debug:
                    publish_debug_exchange.publish("body",headers={"message":allword,
                      "uhid":iosdev.device_token})
                else:
                    publish_release_exchange.publish("body",headers={"message":allword,
                      "uhid":iosdev.device_token})

        user_info=session.query(User).filter(User.uid==post['uid']).first()
        if user_info is None:
            print 'user not found'
            return

        msgbody={
            "touser":'o8Td4jjhPJIsxqZVjuv8xzyLY-hU',
            "msgtype":"text",
            "text":
            {
                 "content":u"%s(%s) 预订了 %s (支付%.2f元)"%(user_info.phone,user_info.nick,
                                                       post['desc'] if 'desc' in post else post['productdesc']
                                                       ,float(post['amount'])/100)
            }
        }
        to_weixin_user=['o8Td4ji85hT5Z9ClI-cT64q9q1ns','o8Td4jjhPJIsxqZVjuv8xzyLY-hU']
        token=weixin.GetAccessToken()
        for u in to_weixin_user:
            msgbody["touser"]=u
            data=weixin.SendMessage(token,msgbody)
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
                    configs.Queue_User,configs.Queue_PassWord,'sys.paylog')
    exchange=Exchange("sys.apn",type='topic',channel=QueueWork.channel,durable=True,delivery_mode=2)
    publish_debug_exchange = Producer(QueueWork.channel,exchange,routing_key='msg.debug')
    publish_release_exchange = Producer(QueueWork.channel,exchange,routing_key='msg.release')
    QueueWork.run()