#coding:utf-8
from datamodel.merchandise import StoreMerchandise,StorePayState
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
def run(mid,people_count,hardwareid,recommend_uid=None):
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
        paystate=StorePayState()
        paystate.orderid=od
        paystate.paystate=0
        paystate.mid=mid
        paystate.uid=BackEndEnvData.uid
        paystate.ex_people=people_count
        paystate.remain=price
        if recommend_uid is not None:
            paystate.recommend_uid=recommend_uid
        session.merge(paystate)
        session.commit()
        mer=MerchantAPI()
        gourl=mer.wap_credit(od,transtime,156,price,str(sm.productcatalog),
                                 "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0)",
                                 sm.productname,sm.productdesc,BackEndEnvData.client_ip,
                                 usr.phone,4,"IMEI:"+hardwareid,"http://%s/payresult/Paybackend"%website_config.hostname,
                                 "http://%s/payresult/Paybackend"%website_config.hostname,"1|2")
        return Res({'gourl':gourl,'orderid':od})
