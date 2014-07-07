#coding:utf-8
import json
from sqlalchemy import or_
from datamodel.merchandise import StoreMerchandise,StorePayState, StoreWeixinNotify, StoreSmsNotify
from datamodel.user import User
from processor.merchandise.count_price import get_price
from tools.helper import Res
from tools.session import CheckSession
import time
import random
from paylib.SmsWap import MerchantAPI
import website_config

__author__ = 'amen'
import BackEndEnvData
import dbconfig
@CheckSession()
def run(mid):
    with dbconfig.Session() as session:
        transtime=int(time.time())
        od=u"%d-%d"%(transtime,random.randint(100, 999))
        paystate=StorePayState()
        paystate.orderid=od
        paystate.paystate=3
        paystate.mid=mid
        paystate.uid=BackEndEnvData.uid
        paystate.remain=0
        session.merge(paystate)
        session.commit()

        #sm=session.query(StoreMerchandise).filter(StoreMerchandise.mid==mid).first()

        return Res({'orderid':od,'msg':u'您已经成功参与“装来信 送酒店”活动，很荣幸您获得茗汉铂尔曼酒店高级房一晚使用权。消费完毕后会有专车在门口迎接您，祝您消费愉快。'})
