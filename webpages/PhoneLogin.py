from tools.session import GenSession
from tools.urls import GetClientWSSite

__author__ = 'amen'
import web
import dbconfig
import WebSiteBasePage
import random
import anyjson
import time
import datamodel.user
import tools.sms

class PhoneLogin(WebSiteBasePage.AutoPage):
    def GET(self):
        params=web.input()
        phone=params.get('phone',None)
        code=params.get('code',None)
        if phone and code:
            vcode=dbconfig.memclient.get(str('vcode:%s'%phone))
            if vcode is None:
                return anyjson.dumps({'error':'time out'})
            if vcode==code:
                with dbconfig.Session() as session:
                    user_info=session.query(datamodel.user.User).filter(datamodel.user.User.phone==phone).first()
                    if user_info is None:
                        user_info=datamodel.user.User()
                        user_info.phone=phone
                        user_info=session.merge(user_info)
                        session.commit()

                    dbconfig.memclient.delete(str('vcode:%s'%phone))
                    session_id=GenSession()
                    TIMEOUTTIME=3600*24*5
                    time_out=time.time()+TIMEOUTTIME
                    dbconfig.memclient.set(str('session:%s'%session_id),{'uid':user_info.uid})
                    return anyjson.dumps({'sessionid':session_id,'timeout':time_out,'ws':GetClientWSSite()})
            else:
                return anyjson.dumps({'error':'code error'})
        tpl=WebSiteBasePage.jinja2_env.get_template('PhoneLogin.html')
        return tpl.render()

class getcode(WebSiteBasePage.AutoPage):
    def GET(self):
        params=web.input()
        phone=params['phone']
        gcode=str(random.randint(1000,9999))
        dbconfig.memclient.set(str('vcode:%s'%phone),gcode,time=600)
        sms_res=None #tools.sms.SendSms(phone,gcode)
        return anyjson.dumps({'code':gcode,'excode':sms_res})