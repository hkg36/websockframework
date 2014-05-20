#coding:utf-8
import urllib
from datamodel.user_circle import CircleDef
from tools.helper import AutoFitJson

__author__ = 'amen'
import json

import qiniu.rs
import web

import WebSiteBasePage
import dbconfig
import datamodel.user
import website_config

class CircleIcon(WebSiteBasePage.AutoPage):
    def GET(self):
        params=web.input(usepage='0')
        policy = qiniu.rs.PutPolicy(dbconfig.qiniuSpace)
        policy.callbackUrl='http://%s/operational_background/CircleIconDone'%website_config.hostname
        policy.callbackBody='{"name":"$(fname)","hash":"$(etag)","width":$(imageInfo.width),"height":$(imageInfo.height),"cid":$(x:cid)}'
        uptoken =policy.token()
        if int(params['usepage'])==0:
            web.header("Content-type","application/json")
            return json.dumps({'token':uptoken})
        tpl=WebSiteBasePage.jinja2_env.get_template('operational/circleicon.html')
        return tpl.render(token=uptoken)
    def POST(self):
        pass

class CircleIconDone(WebSiteBasePage.AutoPage):
    SITE="http://%s.u.qiniudn.com/"%dbconfig.qiniuSpace
    def POST(self):
        imgdata=json.loads(web.data())
        with dbconfig.Session() as session:
            cdef=session.query(CircleDef).filter(CircleDef.cid==imgdata['cid']).first()
            if cdef is None:
                return json.dumps({"errno":1,"error":"cid lost"})
            fileurl=self.SITE+imgdata['hash']
            cdef.icon_url=fileurl
            session.merge(cdef)
            session.commit()
        return json.dumps({"errno":0,"error":"Success","url":fileurl})