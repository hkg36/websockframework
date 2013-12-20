from tools.session import GenSession

__author__ = 'amen'
import web
import dbconfig
import WebSiteBasePage
import random
import anyjson
import time

class PhoneLogin(WebSiteBasePage.AutoPage):
    def GET(self):
        params=web.input()
        phone=params.get('phone',None)
        code=params.get('code',None)
        if phone and code:
            session_id=GenSession()
            time_out=time.time()+3600*24*5
            return anyjson.dumps({'sessionid':session_id,'timeout':time_out,'ws':"ws://127.0.0.1:8000/ws"})
        tpl=WebSiteBasePage.jinja2_env.get_template('PhoneLogin.html')
        return tpl.render()

class getcode(WebSiteBasePage.AutoPage):
    def GET(self):
        params=web.input()
        phone=params['phone']
        gcode=random.randint(1000,9999)
        return anyjson.dumps({'code':gcode})