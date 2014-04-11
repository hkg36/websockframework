#coding:utf-8
from datamodel.merchandise import StoreMerchandise
from datamodel.tenpaylog import *
from datamodel.user import User
from processor.merchandise.count_price import get_price
from tools.helper import Res
from tools.session import CheckSession
import time
import random
import paylib.tenpaylib
import website_config

__author__ = 'amen'
import BackEndEnvData
import dbconfig
@CheckSession()
def run(mid,people_count,hardwareid=None,recommend_uid=None):
    with dbconfig.Session() as session:
        sm=session.query(StoreMerchandise).filter(StoreMerchandise.mid==mid).first()
        if sm is None:
            return Res(errno=2,error="not exist")
        usr=session.query(User).filter(User.uid==BackEndEnvData.uid).first()
        if usr is None:
            return Res(errno=2,error="this bug can not happen")

        price=get_price(sm,people_count=people_count)
        transtime=int(time.time())
        od=u"%d-%d"%(transtime,random.randint(100, 999))

        tp=paylib.tenpaylib.tenpay()
        token_id= tp.init(od,sm.productdesc,1)
        gourl="https://wap.tenpay.com/cgi-bin/wappayv2.0/wappay_gate.cgi?token_id=%s"%token_id

        paystate=TenpayState()
        paystate.orderid=od
        paystate.desc=sm.productdesc
        paystate.mid=mid
        paystate.uid=BackEndEnvData.uid
        paystate.ex_people=people_count
        paystate.remain=price
        if recommend_uid is not None:
            paystate.recm_uid=recommend_uid
        paystate.save()

        return Res({'gourl':gourl,'orderid':od})