#coding:utf-8
from sqlalchemy import and_
from datamodel.Recommend import RecommendUser, RecommendMedia
from tools.helper import AutoFitJson

__author__ = 'amen'
import WebSiteBasePage
import qiniu.rs
import web
import dbconfig
import datamodel.post
import website_config
from webpages.MainPage import pusher
import urllib
import json

def media_token(uid,recommend_uid):
    policy = qiniu.rs.PutPolicy(dbconfig.qiniuSpace)
    policy.callbackUrl='http://%s/recommend/upload/MediaDone'%website_config.hostname
    policy.callbackBody='{"name":"$(fname)","hash":"$(etag)","width":"$(imageInfo.width)","height":"$(imageInfo.height)",' +\
                        '"length":"$(x:length)","uid":%d,"recommend_uid":%d,"filetype":"$(x:filetype)"}'%(uid,recommend_uid)
    return policy.token()
class Media(WebSiteBasePage.AutoPage):
    def GET(self):
        params=web.input(usepage='0')
        sessionid=params.get('sessionid',None)
        uid=int(params.get('uid',0))
        recommend_uid=int(params.get('recommend_uid',0))
        if sessionid is None:
            return "No Session id"
        data=dbconfig.redisdb.get(str('session:%s'%sessionid))
        if data is None:
            return {"errno":1,"error":"session not found","result":{}}
        data=json.loads(data)
        if data['uid']!=uid and data['uid']!=recommend_uid:
            return "user is error()"
        with dbconfig.Session() as session:
            ru=session.query(RecommendUser).filter(and_(RecommendUser.uid==uid,RecommendUser.recommend_uid==recommend_uid)).first()
            if ru is None:
                return "RecommendUser not exists"
        uptoken = media_token(uid,recommend_uid)
        if int(params['usepage'])==0:
            web.header("Content-type","application/json")
            return json.dumps({'token':uptoken})
        tpl=WebSiteBasePage.jinja2_env.get_template('upload/PostEx.html')
        return tpl.render(token=uptoken)

class MediaDone(WebSiteBasePage.AutoPage):
    def POST(self):
        imgdata=json.loads(web.data())
        with  dbconfig.Session() as session:
            rm=RecommendMedia()
            rm.uid=imgdata['uid']
            rm.recommend_uid=imgdata['recommend_uid']
            fileurl=dbconfig.qiniuDownLoadLinkHead+imgdata['hash']
            filetype=int(imgdata['filetype'])
            if filetype==1:
                rm.picture=fileurl
                rm.width=imgdata['width']
                rm.height=imgdata['height']
            elif filetype==2:
                rm.voice=fileurl
                rm.length=imgdata['length']
            elif filetype==3:
                rm.video=fileurl
                rm.length=imgdata['length']
            rm=session.merge(rm)
            session.query(RecommendUser).filter(and_(RecommendUser.uid==imgdata['uid'],RecommendUser.recommend_uid==imgdata['recommend_uid'])).\
                update({RecommendUser.media_count:RecommendUser.media_count+1})
            session.commit()

            return json.dumps({"errno":0,"error":"Success","result":{"url":fileurl,'did':rm.did}},cls=AutoFitJson)
