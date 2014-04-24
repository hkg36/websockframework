#coding:utf-8
import json
import urllib2
from poster.encode import multipart_encode, MultipartParam
import WebSiteBasePage
import web
import tools.weixin

__author__ = 'amen'
class postimg(WebSiteBasePage.AutoPage):
    def GET(self):
        tpl=WebSiteBasePage.jinja2_env.get_template("weixin/uploadimg.html")
        return tpl.render()
    def POST(self):
        params=web.input(uploadimg={})
        to_uid=params['id']
        uploadimg=params['uploadimg']
        datagen, headers = multipart_encode([MultipartParam("name",value=uploadimg.value,filename=uploadimg.filename,filetype=uploadimg.type)])
        token=tools.weixin.GetAccessToken()
        type='image'
        request = urllib2.Request("http://file.api.weixin.qq.com/cgi-bin/media/upload?access_token=%s&type=%s"%(token,type), datagen, headers)
        data=json.loads(urllib2.urlopen(request).read())
        return tools.weixin.SendMessage(token,{
            "touser":to_uid,
            "msgtype":"image",
            "image":
            {
              "media_id":data['media_id']
            }
        })
