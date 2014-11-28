#coding:utf-8
import urllib
from tools.helper import AutoFitJson
import codecs
from tools.json_tools import DefJsonEncoder

__author__ = 'amen'
import json
import web

import WebSiteBasePage
import dbconfig
import qiniu
import website_config
import os

class Version(WebSiteBasePage.AutoPage):
    def GET(self):
        uptoken =dbconfig.qiniuAuth.upload_token(dbconfig.qiniuSpace,policy={"callbackUrl":'http://%s/android/VersionDone'%website_config.hostname,
                                                                             "callbackBody":'{"name":"http://$(bucket).qiniudn.com/$(key)","hash":"$(etag)",' \
                            '"verCode":"$(x:verCode)","verName":"$(x:verName)","Info":"$(x:Info)"}'})

        tpl=WebSiteBasePage.jinja2_env.get_template('android/newversion.html')
        return tpl.render(token=uptoken)
class DeleteVersion(WebSiteBasePage.AutoPage):
    def GET(self):
        try:
            os.remove('static/android/version.js')
        except Exception,e:
            pass
        qiniubk=qiniu.BucketManager(dbconfig.qiniuAuth)
        qiniubk.delete(dbconfig.qiniuSpace,'laixin_newversion.apk')
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
        return DefJsonEncoder.encode({"url":'http://%s/static/android/version.js'%website_config.hostname})
