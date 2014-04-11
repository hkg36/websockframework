#coding:utf-8
import json
import WebSiteBasePage
import web
import paylib.tenpaylib
import datamodel.tenpaylog
import datetime
from tools.helper import AutoFitJson
from webpages.MainPage import pusher

__author__ = 'amen'
class TenpayNotifyCallBack(WebSiteBasePage.AutoPage):
    def GET(self):
        if self.Check():
            return "success"
        else:
            return u"fail"
    def POST(self):
        if self.Check():
            return "success"
        else:
            return u"fail"
    def Check(self):
        all=web.input()
        tp=paylib.tenpaylib.tenpay()
        if tp.VerifySign(all):
            ps=datamodel.tenpaylog.TenpayState.objects(orderid=all['sp_billno']).first()
            new_pay_state=1 if int(all['pay_result'])==0 else -1
            if ps.paystate==new_pay_state:
                return True
            ps.paystate=new_pay_state
            ps.paytime=datetime.datetime.now()
            ps.transaction_id=all['transaction_id']
            ps.remain=all['total_fee']
            ps.save()

            pl=datamodel.tenpaylog.TenpayLog(ps)
            pl.pay_info=all.get('pay_info')
            pl.bank_type=all.get('bank_type')
            pl.bank_billno=all.get('bank_billno')
            pl.time_end=all.get('time_end')
            pl.purchase_alias=all.get('purchase_alias')
            pl.save()

            try:
                json_post=json.dumps(pl.toJson(),cls=AutoFitJson,ensure_ascii=False,separators=(',', ':'))
                pusher.rawPush(routing_key='sys.paylog',headers={},body=json_post)
            except Exception,e:
                print e
            return True
        else:
            return False
class TenpayCallBack(WebSiteBasePage.AutoPage):
    def GET(self):
        all=web.input()
        tp=paylib.tenpaylib.tenpay()
        signParameterArray = [
				"ver",
				"charset",
				"pay_result",
				"transaction_id",
				"sp_billno",
				"total_fee",
				"fee_type",
				"bargainor_id",
				"attach",
				"time_end"
		]
        signParameterArray.sort()
        signed=all['sign']
        if signed==tp.GetSignAsKeyList(all,signParameterArray):
            tpl=WebSiteBasePage.jinja2_env.get_template('paysuccess.html')
            return tpl.render()
        else:
            return "fail"