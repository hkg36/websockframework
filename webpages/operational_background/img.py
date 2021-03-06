#coding:utf-8
import urllib
from tools.helper import AutoFitJson
from tools.json_tools import DefJsonEncoder

__author__ = 'amen'
import json
import obtools
import web

import WebSiteBasePage
import dbconfig

class Image(WebSiteBasePage.AutoPage):
    @obtools.AccessControl()
    def GET(self):
        params=web.input(usepage='0')
        uptoken =dbconfig.qiniuAuth.upload_token(dbconfig.qiniuSpace,policy={"returnBody":'{"errno":0,"error":"Success","url":"http://$(bucket).qiniudn.com/$(key)"}'})
        if int(params['usepage'])==0:
            web.header("Content-type","application/json")
            return DefJsonEncoder.encode({'token':uptoken})
        tpl=WebSiteBasePage.jinja2_env.get_template('upload/UploadImage.html')
        return tpl.render(token=uptoken)
    def POST(self):
        pass
