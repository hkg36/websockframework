#coding:utf-8
from tools.helper import AutoFitJson

__author__ = 'amen'
import WebSiteBasePage
import web
import dbconfig
import datamodel.post
import website_config
from webpages.MainPage import pusher
import urllib
import json
import tools.crypt_session

def post_token(uid):
    return dbconfig.qiniuAuth.upload_token(dbconfig.qiniuSpace,policy={"callbackUrl":'http://%s/upload/PostDone'%website_config.hostname,
                                                                       "callbackBody":'{"name":"$(fname)","hash":"$(etag)","width":"$(imageInfo.width)","height":"$(imageInfo.height)",' +\
                        '"gid":"$(x:gid)","content":"$(x:content)","length":"$(x:length)","uid":%d,"filetype":"$(x:filetype)"}'%uid})
class Post(WebSiteBasePage.AutoPage):
    def GET(self):
        params=web.input(usepage='0')
        sessionid=params.get('sessionid',None)
        if sessionid is None:
            return "No Session id"
        data=tools.crypt_session.DecodeCryptSession(sessionid)
        if data is None:
            data=dbconfig.redisdb.get(str('session:%s'%sessionid))
            if data:
                data=json.loads(data)
        if data is None:
            return {"errno":1,"error":"session not found","result":{}}
        uptoken = post_token(data['uid'])
        if int(params['usepage'])==0:
            web.header("Content-type","application/json")
            return json.dumps({'token':uptoken})
        tpl=WebSiteBasePage.jinja2_env.get_template('upload/Post.html')
        return tpl.render(token=uptoken)
    def POST(self):
        pass

class PostDone(WebSiteBasePage.AutoPage):
    def POST(self):
        imgdata=json.loads(web.data())
        with  dbconfig.Session() as session:
            newpost=datamodel.post.Post()
            newpost.uid=imgdata['uid']
            newpost.group_id=imgdata['gid']
            content_data=imgdata.get('content')
            if content_data:
                newpost.content=urllib.unquote_plus(content_data.encode('ascii')).decode('utf-8')
            fileurl=dbconfig.qiniuDownLoadLinkHead+imgdata['hash']
            filetype=int(imgdata['filetype'])
            if filetype==1:
                newpost.picture=fileurl
                newpost.width=imgdata['width']
                newpost.height=imgdata['height']
            elif filetype==2:
                newpost.voice=fileurl
                newpost.length=imgdata['length']
            elif filetype==3:
                newpost.video=fileurl
                newpost.length=imgdata['length']
            newpost=session.merge(newpost)
            session.commit()
            try:
                json_post=json.dumps(newpost.toJson(),cls=AutoFitJson)
                pusher.rawPush(routing_key='sys.post_to_notify',headers={},body=json_post)
            except Exception,e:
                return json.dumps({'errno':5,'error':str(e)})

            return json.dumps({"errno":0,"error":"Success","result":{"url":fileurl,'postid':newpost.postid}},cls=AutoFitJson)

def postex_token(postid):
    policy = qiniu.rs.PutPolicy(dbconfig.qiniuSpace)
    policy.callbackUrl='http://%s/upload/PostExDone'%website_config.hostname
    policy.callbackBody='{"name":"$(fname)","hash":"$(etag)","width":"$(imageInfo.width)","height":"$(imageInfo.height)",' +\
                        '"length":"$(x:length)","postid":%d,"filetype":"$(x:filetype)"}'%postid
    return policy.token()
class PostEx(WebSiteBasePage.AutoPage):
    def GET(self):
        params=web.input(usepage='0')
        sessionid=params.get('sessionid',None)
        postid=params.get('postid',None)
        if sessionid is None:
            return "No Session id"
        if postid is None:
            return "No Post id"
        data=tools.crypt_session.DecodeCryptSession(sessionid)
        if data is None:
            data=dbconfig.redisdb.get(str('session:%s'%sessionid))
            if data:
                data=json.loads(data)
        if data is None:
            return {"errno":1,"error":"session not found","result":{}}
        with dbconfig.Session() as session:
            oldpost=session.query(datamodel.post.Post).filter(datamodel.post.Post.postid==postid).first()
            if oldpost is None or oldpost.uid!=data['uid']:
                return "post not exists or not yours"
        uptoken = postex_token(int(postid))
        if int(params['usepage'])==0:
            web.header("Content-type","application/json")
            return json.dumps({'token':uptoken})
        tpl=WebSiteBasePage.jinja2_env.get_template('upload/PostEx.html')
        return tpl.render(token=uptoken)

class PostExDone(WebSiteBasePage.AutoPage):
    def POST(self):
        imgdata=json.loads(web.data())
        with  dbconfig.Session() as session:
            newpostex=datamodel.post.PostExData()
            newpostex.postid=imgdata['postid']
            fileurl=dbconfig.qiniuDownLoadLinkHead+imgdata['hash']
            filetype=int(imgdata['filetype'])
            if filetype==1:
                newpostex.picture=fileurl
                newpostex.width=imgdata['width']
                newpostex.height=imgdata['height']
            elif filetype==2:
                newpostex.voice=fileurl
                newpostex.length=imgdata['length']
            elif filetype==3:
                newpostex.video=fileurl
                newpostex.length=imgdata['length']
            newpostex=session.merge(newpostex)
            session.query(datamodel.post.Post).filter(datamodel.post.Post.postid==imgdata['postid']).\
                update({datamodel.post.Post.excount:datamodel.post.Post.excount+1})
            session.commit()

            return json.dumps({"errno":0,"error":"Success","result":{"url":fileurl,'did':newpostex.did}},cls=AutoFitJson)