#coding:utf-8
import web

import WebSiteBasePage
from MainPage import pusher


class TestWebsocketPush(WebSiteBasePage.AutoPage):
    def GET(self):
        return self.buildpage()
    def POST(self):
        post_params=web.input()
        post_data=post_params['content']
        queueid=post_params['queueid']
        connectid=post_params['connectid']
        try:
            pusher.Push(queueid,connectid,post_data)
            return self.buildpage()
        except Exception,e:
            return self.buildpage(str(e))
    def buildpage(self,extinfo=''):
        tpl=WebSiteBasePage.jinja2_env.get_template('WebsocketPush.html')
        return tpl.render()
