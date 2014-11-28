#coding:utf-8
import urllib
from datamodel.user_circle import CircleDef
from tools.helper import AutoFitJson
from tools.json_tools import DefJsonEncoder

__author__ = 'amen'
import json
import web

import WebSiteBasePage
import dbconfig
import website_config

class CircleIcon(WebSiteBasePage.AutoPage):
    def GET(self):
        params=web.input(usepage='0')
        uptoken =dbconfig.qiniuAuth.upload_token(dbconfig.qiniuSpace,policy={"callbackUrl":'http://%s/operational_background/CircleIconDone'%website_config.hostname,
                                                                             "callbackBody":'{"name":"$(fname)","hash":"$(etag)","width":$(imageInfo.width),"height":$(imageInfo.height),"cid":$(x:cid)}'})
        if int(params['usepage'])==0:
            web.header("Content-type","application/json")
            return DefJsonEncoder.encode({'token':uptoken})
        tpl=WebSiteBasePage.jinja2_env.get_template('operational/circleicon.html')
        return tpl.render(token=uptoken)
    def POST(self):
        pass

class CircleIconDone(WebSiteBasePage.AutoPage):
    def POST(self):
        imgdata=json.loads(web.data())
        with dbconfig.Session() as session:
            cdef=session.query(CircleDef).filter(CircleDef.cid==imgdata['cid']).first()
            if cdef is None:
                return DefJsonEncoder.encode({"errno":1,"error":"cid lost"})
            fileurl=dbconfig.qiniuDownLoadLinkHead+imgdata['hash']
            cdef.icon_url=fileurl
            session.merge(cdef)
            session.commit()
        return DefJsonEncoder.encode({"errno":0,"error":"Success","url":fileurl})