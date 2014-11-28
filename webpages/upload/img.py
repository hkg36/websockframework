#coding:utf-8
import urllib
from tools.helper import AutoFitJson

__author__ = 'amen'
import json
import web

import WebSiteBasePage
import dbconfig
import tools.crypt_session

class Image(WebSiteBasePage.AutoPage):
    def GET(self):
        params=web.input(usepage='0')
        sessionid=params.get('sessionid',None)
        if sessionid is None:
            return "No Session id"
        data=tools.crypt_session.DecodeCryptSession(sessionid)
        if data is None:
            data=dbconfig.redisdb.get(str('session:%s'%sessionid))
        if data is None:
            return {"errno":1,"error":"session not found","result":{}}
        uptoken = dbconfig.qiniuAuth.upload_token(dbconfig.qiniuSpace,policy={"returnBody":'{"errno":0,"error":"Success","url":"http://$(bucket).qiniudn.com/$(key)"}'})
        if int(params['usepage'])==0:
            web.header("Content-type","application/json")
            return json.dumps({'token':uptoken})
        tpl=WebSiteBasePage.jinja2_env.get_template('upload/HeadImg.html')
        return tpl.render(token=uptoken)
    def POST(self):
        pass
