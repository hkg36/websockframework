#coding:utf-8
import urllib
from tools.helper import AutoFitJson
from tools.json_tools import DefJsonEncoder

__author__ = 'amen'
import json
import obtools
import qiniu.rs
import web

import WebSiteBasePage
import dbconfig
import datamodel.user
import website_config

class Image(WebSiteBasePage.AutoPage):
    @obtools.AccessControl()
    def GET(self):
        params=web.input(usepage='0')
        policy = qiniu.rs.PutPolicy(dbconfig.qiniuSpace)
        policy.returnBody='{"errno":0,"error":"Success","url":"http://$(bucket).qiniudn.com/$(key)"}'
        uptoken =policy.token()
        if int(params['usepage'])==0:
            web.header("Content-type","application/json")
            return DefJsonEncoder.encode({'token':uptoken})
        tpl=WebSiteBasePage.jinja2_env.get_template('upload/HeadImg.html')
        return tpl.render(token=uptoken)
    def POST(self):
        pass
