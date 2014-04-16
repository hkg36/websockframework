#coding:utf-8
import json
import WebSiteBasePage
import web
from datamodel.events import Events
from datamodel.merchandise import StorePayState, StoreMerchandise, StorePayLog
from datamodel.tenpaylog import TenpayLog
from paylib.SmsWap import MerchantAPI
import dbconfig
import datetime
from tools.helper import AutoFitJson
from webpages.MainPage import pusher
import traceback

__author__ = 'amen'
class TestPushEPay(WebSiteBasePage.AutoPage):
    def GET(self):
        try:
            params=web.input()
            payid=params.get("payid")
            with dbconfig.Session() as session:
                paylog=session.query(StorePayLog).filter(StorePayLog.payid==payid).first()

                json_post=json.dumps(paylog.toJson(),cls=AutoFitJson,ensure_ascii=False)
                pusher.rawPush(routing_key='sys.paylog',headers={},body=json_post)
                return "ok"
        except Exception,e:
            return False
class TestPushTenpay(WebSiteBasePage.AutoPage):
    def GET(self):
        try:
            params=web.input()
            payid=int(params.get("payid"))
            paylog=TenpayLog.objects(payid=payid).first()

            json_post=json.dumps(paylog.toJson(),cls=AutoFitJson,ensure_ascii=False)
            pusher.rawPush(routing_key='sys.paylog',headers={},body=json_post)
            return "ok"
        except Exception,e:
            return traceback.format_exc()