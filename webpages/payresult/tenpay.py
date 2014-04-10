#coding:utf-8
import json
import WebSiteBasePage
import web
import paylib.tenpaylib

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
        return tp.VerifySign(all)
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