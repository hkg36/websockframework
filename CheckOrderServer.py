#coding:utf-8
import json
from sqlalchemy import and_
from datamodel.merchandise import StorePayState, StoreMerchandise, StorePayLog
from tools.helper import AutoFitJson
from webpages.MainPage import pusher

__author__ = 'amen'
import dbconfig
from paylib.SmsWap import MerchantAPI
import datetime
import time
mer=MerchantAPI()
while True:
    time_max=datetime.datetime.now()-datetime.timedelta(seconds=10)
    time_min=time_max-datetime.timedelta(hours=1)
    with dbconfig.Session() as session:
        all_pay=session.query(StorePayState).filter(and_(StorePayState.paystate==0,StorePayState.create_time<time_max,StorePayState.create_time>time_min)).all()
        #all_pay=session.query(StorePayState).filter(StorePayState.paystate==0).all()
        for pay in all_pay:
            payinfo=mer.QueryPay(pay.orderid,"")
            print(payinfo)
            if "error_code" in payinfo:
                pay.paystate=-1
                session.merge(pay)
            else:
                pay.paystate=1
                pay.paytime=datetime.datetime.now()
                pay.yborderid=payinfo['yborderid']
                pay.remain=payinfo['amount']
                session.merge(pay)
                sm=session.query(StoreMerchandise).filter(StoreMerchandise.mid==pay.mid).first()
                log=StorePayLog(sm,pay)
                log=session.merge(log)
                session.commit()

                try:
                    json_post=json.dumps(log.toJson(),cls=AutoFitJson,ensure_ascii=False)
                    pusher.rawPush(routing_key='sys.paylog',headers={},body=json_post)
                except Exception,e:
                    pass
        session.commit()
    time.sleep(10)