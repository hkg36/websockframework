__author__ = 'amen'

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
from webpages.MainPage import pusher
import tools.weixin

__author__ = 'amen'
class now_access_token(WebSiteBasePage.AutoPage):
    def GET(self):
        return tools.weixin.GetAccessToken()
class test(WebSiteBasePage.AutoPage):
    def GET(self):
        return web.ctx.get('ip')