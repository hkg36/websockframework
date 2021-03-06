import random
import time
from datamodel.merchandise import StoreMerchandise, StorePayState
from datamodel.user import User
from paylib.SmsWap import MerchantAPI
from processor.merchandise.count_price import get_price
from tools.helper import Res
from tools.session import CheckSession
import website_config

__author__ = 'amen'
import BackEndEnvData
import dbconfig
@CheckSession()
def run(cardid,mid,people_count,hardwareid,recommend_uid=None):
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
        paystate.remain=price
        paystate.ex_people=people_count
        if recommend_uid is not None:
            paystate.recommend_uid=recommend_uid
        session.merge(paystate)
        session.commit()
        mer=MerchantAPI()
        res=mer.BindPaysignAsync(cardid,od,transtime,156,price,str(sm.productcatalog),
                                 sm.productname,sm.productdesc,BackEndEnvData.client_ip,
                                 usr.phone,4,"IMEI:"+hardwareid,"http://%s/payresult/Paybackend"%website_config.hostname,
                                 "http://%s/payresult/Paybackend"%website_config.hostname)
        if res.get('error_code',None) is None:
            if res['accept']==1:
                return Res({'orderid':od})
            else:
                return Res(errno=3,error="pay not accept")
        else:
            return Res({'src_error':res},errno=3,error="pay fail")