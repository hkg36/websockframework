#coding:utf-8
import time
from kombu import Exchange, Producer
from sqlalchemy import and_, or_

from datamodel.ios import IOSDevice
from datamodel.merchandise import StoreWeixinNotify, StoreSmsNotify
from datamodel.user import User
from tools.helper import AutoFitJson, DefJsonEncoder


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
    #print body
    post=json.loads(body)
    toids={post['uid'],post['recommend_uid']}
    product_name=post['desc'] if 'desc' in post else post['productdesc']
    with dbconfig.Session() as session:
        conns=session.query(ConnectionInfo).filter(ConnectionInfo.uid.in_(list(toids))).all()
        if len(conns)>0:
            to_push=DefJsonEncoder.encode({"push":True,
                                        "type":"paylog",
                                        "data":{
                                            "log":post
                                        }
                                    })
            for conn in conns:
                toids.remove(conn.uid)
                QueueWork.producer.publish(body=to_push,delivery_mode=2,headers={"connid":conn.connection_id},
                                              routing_key=conn.queue_id,
                                              compression='gzip',
                                              exchange="front_end")
        iosdevs=session.query(IOSDevice).filter(IOSDevice.uid.in_(list(toids))).all()
        if len(iosdevs)>0:
            try:
                if post['paystate']==1:
                    allword=u"订单[%s] %.2f元,已支付成功,详情可查看订单历史"%(product_name,float(post['amount'])/100)
                else:
                    allword=u"订单[%s] %.2f元,支付失败,详情可查看订单历史"%(product_name,float(post['amount'])/100)
                for iosdev in iosdevs:
                    if iosdev.is_debug:
                        publish_debug_exchange.publish("body",headers={"message":allword,
                          "uhid":iosdev.device_token,"badge":iosdev.badge+1})
                    else:
                        publish_release_exchange.publish("body",headers={"message":allword,
                          "uhid":iosdev.device_token,"badge":iosdev.badge+1})
                    iosdev.badge=iosdev.badge+1
                    iosdev=session.merge(iosdev)
                session.commit()
            except Exception,e:
                pass

        if post['paystate']!=1:
            return
        user_info=session.query(User).filter(User.uid==post['uid']).first()
        if user_info is None:
            #print 'user not found'
            return

        msg_content=u"%s(%s) 预订了 %s (%s 支付%.2f元)"%(user_info.phone,user_info.nick,product_name,
                                                          time.strftime("%m-%d %H:%M",time.localtime(post['create_time'])),float(post['amount'])/100)

        to_sendsms=session.query(StoreSmsNotify).filter(or_(StoreSmsNotify.mid==0,StoreSmsNotify.mid==None,StoreSmsNotify.mid==post['mid'])).all()
        for ssn in to_sendsms:
            QueueWork.producer.publish(DefJsonEncoder.encode({'content':msg_content,'phone':ssn.phone}),routing_key='sms.code',exchange='sys.sms')

        to_notifys=session.query(StoreWeixinNotify).filter(or_(StoreWeixinNotify.mid==0,StoreWeixinNotify.mid==None,StoreWeixinNotify.mid==post['mid'])).all()
        to_weixin_user=set()
        for noti_one in to_notifys:
            to_weixin_user.add(noti_one.openid)
        if len(to_weixin_user)==0:
            return
        send_weixin.publish(DefJsonEncoder.encode({
            'weixin_users':list(to_weixin_user),
            'content':msg_content
        }))

exchange=None
publish_debug_exchange = None
publish_release_exchange = None
send_weixin=None

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
                    configs.Queue_User,configs.Queue_PassWord,'sys.paylog',exchange_name="system")
    exchange=Exchange("sys.apn",type='topic',channel=QueueWork.channel,durable=True,delivery_mode=2)
    publish_debug_exchange = Producer(QueueWork.channel,exchange,routing_key='msg.debug')
    publish_release_exchange = Producer(QueueWork.channel,exchange,routing_key='msg.release')
    send_weixin = Producer(QueueWork.channel,routing_key='sys.sendweixin')

    QueueWork.run()