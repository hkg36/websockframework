from tools.helper import AutoFitJson

__author__ = 'amen'
import WebSiteBasePage
import qiniu.rs
import web
import anyjson
import dbconfig
import datamodel.post
import website_config
from webpages.MainPage import pusher
import urllib
import json

class Post(WebSiteBasePage.AutoPage):
    def GET(self):
        params=web.input(usepage='0')
        sessionid=params.get('sessionid',None)
        if sessionid is None:
            return "No Session id"
        data=dbconfig.memclient.get(str('session:%s'%sessionid))
        if data is None:
            return {"errno":1,"error":"session not found","result":{}}
        policy = qiniu.rs.PutPolicy(dbconfig.qiniuSpace)
        policy.callbackUrl='http://%s/upload/PostDone'%website_config.hostname
        policy.callbackBody='{"name":"$(fname)","hash":"$(etag)","width":$(imageInfo.width),"height":$(imageInfo.height),' +\
                            '"gid":"$(x:gid)","content":"$(x:content)","length":"$(x:length)","uid":%d,"filetype":"$(x:filetype)"}'%data['uid']
        uptoken = policy.token()
        if int(params['usepage'])==0:
            web.header("Content-type","application/json")
            return anyjson.dumps({'token':uptoken})
        tpl=WebSiteBasePage.jinja2_env.get_template('upload/Post.html')
        return tpl.render(token=uptoken)
    def POST(self):
        pass

class PostDone(WebSiteBasePage.AutoPage):
    SITE="http://%s.u.qiniudn.com/"%dbconfig.qiniuSpace
    def POST(self):
        imgdata=anyjson.loads(web.data())
        with  dbconfig.Session() as session:
            newpost=datamodel.post.Post()
            newpost.uid=imgdata['uid']
            newpost.group_id=imgdata['gid']
            content_data=imgdata.get('content')
            if content_data:
                newpost.content=urllib.unquote_plus(content_data.encode('ascii')).decode('utf-8')
            fileurl=self.SITE+imgdata['hash']
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