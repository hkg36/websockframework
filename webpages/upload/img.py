#coding:utf-8
import urllib
from tools.helper import AutoFitJson

__author__ = 'amen'
import json

import qiniu.rs
import web

import WebSiteBasePage
import dbconfig
import datamodel.user
import website_config

class Image(WebSiteBasePage.AutoPage):
    SITE="http://%s.u.qiniudn.com/"%dbconfig.qiniuSpace
    def GET(self):
        params=web.input(usepage='0')
        sessionid=params.get('sessionid',None)
        if sessionid is None:
            return "No Session id"
        data=dbconfig.redisdb.get(str('session:%s'%sessionid))
        if data is None:
            return {"errno":1,"error":"session not found","result":{}}
        policy = qiniu.rs.PutPolicy(dbconfig.qiniuSpace)
        policy.returnBody='{"errno":0,"error":"Success","url":"%s$(etag)"}'%self.SITE
        uptoken =policy.token()
        if int(params['usepage'])==0:
            web.header("Content-type","application/json")
            return json.dumps({'token':uptoken})
        tpl=WebSiteBasePage.jinja2_env.get_template('upload/HeadImg.html')
        return tpl.render(token=uptoken)
    def POST(self):
        pass
