#coding:utf-8
import json
import WebSiteBasePage
import web
from datamodel.events import Events
from datamodel.merchandise import StorePayState, StoreMerchandise, StorePayLog
from paylib.SmsWap import MerchantAPI
import dbconfig
import datetime
from tools.helper import AutoFitJson
from tools.json_tools import DefJsonEncoder
from webpages.MainPage import pusher

__author__ = 'amen'
class Paybackend(WebSiteBasePage.AutoPage):
    def GET(self):
        if self.Check():
            tpl=WebSiteBasePage.jinja2_env.get_template('paysuccess.html')
            return tpl.render()
        else:
            return u"fail"
    def POST(self):
        self.Check()
    def Check(self):
        params=web.input()
        data=params['data']
        encryptkey=params['encryptkey']

        mer=MerchantAPI()
        result=mer.result_decrypt({'data':data,
                            'encryptkey':encryptkey})
        with dbconfig.Session() as session:
            paystate=session.query(StorePayState).filter(StorePayState.orderid==result['orderid']).first()
            if paystate.paystate==1:
                return True
            paystate.paystate=1 if result['status']==1 else -1
            paystate.paytime=datetime.datetime.now()
            paystate.yborderid=result['yborderid']
            paystate.remain=result['amount']
            session.merge(paystate)

            sm=session.query(StoreMerchandise).filter(StoreMerchandise.mid==paystate.mid).first()
            log=StorePayLog(sm,paystate)
            log=session.merge(log)
            session.commit()

            try:
                json_post=DefJsonEncoder.encode(log.toJson())
                pusher.rawPush(exchange="system",routing_key='sys.paylog',headers={},body=json_post)
                return True
            except Exception,e:
                return False