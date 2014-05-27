#coding:utf-8
import urllib
from tools.helper import AutoFitJson
import codecs

__author__ = 'amen'
import json

import qiniu.rs
import web

import WebSiteBasePage
import dbconfig
import datamodel.user
import website_config
import os

class Version(WebSiteBasePage.AutoPage):
    def GET(self):
        policy = qiniu.rs.PutPolicy(dbconfig.qiniuSpace)
        policy.callbackUrl='http://%s/android/VersionDone'%website_config.hostname
        policy.callbackBody='{"name":"http://$(bucket).qiniudn.com/$(key)","hash":"$(etag)",' \
                            '"verCode":"$(x:verCode)","verName":"$(x:verName)","Info":"$(x:Info)"}'
        uptoken =policy.token()

        tpl=WebSiteBasePage.jinja2_env.get_template('android/newversion.html')
        return tpl.render(token=uptoken)
class DeleteVersion(WebSiteBasePage.AutoPage):
    def GET(self):
        try:
            os.remove('static/android/version.js')
        except Exception,e:
            pass
        qnclient=qiniu.rs.Client()
        qnclient.delete(dbconfig.qiniuSpace,'laixin_newversion.apk')
        return "0"
class VersionDone(WebSiteBasePage.AutoPage):
    def POST(self):
        backdata=json.loads(web.data())
        verCode=int(backdata['verCode'])
        verName=urllib.unquote_plus(backdata['verName'].encode('ascii')).decode('utf-8')
        Info=urllib.unquote_plus(backdata['Info'].encode('ascii')).decode('utf-8')
        file=backdata['name']

        fout= codecs.open('static/android/version.js','w','utf-8')
        json.dump({'verCode':verCode,'verName':verName,'Info':Info,'url':file},fout,ensure_ascii=False)
        fout.close()
        return json.dumps({"url":'http://%s/static/android/version.js'%website_config.hostname})
