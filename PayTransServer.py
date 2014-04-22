#coding:utf-8
import time
from kombu import Exchange, Producer
from sqlalchemy import and_, or_

from datamodel.ios import IOSDevice
from datamodel.merchandise import StoreWeixinNotify
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
    #print body
    post=json.loads(body)
    toids={post['uid'],post['recommend_uid']}
    product_name=post['desc'] if 'desc' in post else post['productdesc']
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
        to_notifys=session.query(StoreWeixinNotify).filter(or_(StoreWeixinNotify.mid==0,StoreWeixinNotify.mid==None,StoreWeixinNotify.mid==post['mid'])).all()
        to_weixin_user=set()
        for noti_one in to_notifys:
            to_weixin_user.add(noti_one.openid)
        if len(to_weixin_user)==0:
            return
        msgbody={
            "touser":'o8Td4jjhPJIsxqZVjuv8xzyLY-hU',
            "msgtype":"text",
            "text":
            {
                 "content":u"%s(%s) 预订了 %s (%s 支付%.2f元) 可以领取价值1288的红酒一瓶！！"%(user_info.phone,user_info.nick,product_name,
                                                          time.strftime("%m-%d %H:%M",time.localtime(post['create_time'])),float(post['amount'])/100)
            }
        }
        """to_weixin_user=['o8Td4ji85hT5Z9ClI-cT64q9q1ns',
                        'o8Td4jjhPJIsxqZVjuv8xzyLY-hU',
                        'o8Td4jrfHI_jPTzq0okL6BULRQtY',
                        'o8Td4jtb77tcNS4vHBIvR6KFh2Wg',
                        'o8Td4jqgQgocVfGbSNzRBn_i7kcw']"""
        token=weixin.GetAccessToken()
        for u in to_weixin_user:
            msgbody["touser"]=u
            data=weixin.SendMessage(token,msgbody)
            #print data
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