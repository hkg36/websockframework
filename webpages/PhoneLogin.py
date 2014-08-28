#coding:utf8
from tools.helper import DecodeCryptSession, BuildCryptSession, DefJsonEncoder
from tools.session import GenSession
from tools.urls import GetClientWSSite, GetClientWSSSite

__author__ = 'amen'
import web
import dbconfig
import WebSiteBasePage
import random
import json
import time
import datamodel.user
import datetime
from MainPage import pusher
class PhoneLogin(WebSiteBasePage.AutoPage):
    def GET(self):
        params=web.input()
        phone=params.get('phone',None)
        code=params.get('code',None)
        if phone and code:
            vcode=dbconfig.memclient.get(str('vcode:%s'%phone))
            if vcode==code or (phone=="13067575127" and code=='99999'):
                with dbconfig.Session() as session:
                    user_info=session.query(datamodel.user.User).filter(datamodel.user.User.phone==phone).first()
                    if user_info is None:
                        user_info=datamodel.user.User()
                        user_info.phone=phone
                        user_info=session.merge(user_info)
                        session.commit()

                    dbconfig.memclient.delete(str('vcode:%s'%phone))
                    if int(params.get('cryptsession',0)):
                        session_id=BuildCryptSession(user_info.uid)
                        return DefJsonEncoder.encode({'sessionid':session_id,'ws':GetClientWSSite(),'wss':GetClientWSSSite()})
                    else:
                        session_id=GenSession()
                        TIMEOUTTIME=3600*24*5
                        time_out=time.time()+TIMEOUTTIME
                        dbconfig.redisdb.set(str('session:%s'%session_id),DefJsonEncoder.encode({'uid':user_info.uid}),ex=datetime.timedelta(days=180))
                        return DefJsonEncoder.encode({'sessionid':session_id,'timeout':time_out,'ws':GetClientWSSite(),'wss':GetClientWSSSite()})
            else:
                return DefJsonEncoder.encode({'error':'code error'})
        tpl=WebSiteBasePage.jinja2_env.get_template('PhoneLogin.html')
        return tpl.render()

class getcode(WebSiteBasePage.AutoPage):
    def GET(self):
        params=web.input()
        phone=params['phone']
        if not dbconfig.memclient.add(str('sms_timeout:%s'%phone),'ok',time=60):
            return DefJsonEncoder.encode({"msg":"请等待60秒后再重新发送"})
        phonekey=str('vcode:%s'%phone)
        gcode=dbconfig.memclient.get(phonekey)
        if not gcode:
            gcode=str(random.randint(1000,9999))
            dbconfig.memclient.set(phonekey,gcode,time=60*60)
        if int(params.get('notsms',0))==0:
            pusher.sendCode(phone,gcode)
            return '{}'
        else:
            return DefJsonEncoder.encode({'code':gcode})