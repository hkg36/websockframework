#coding:utf-8
from tools.helper import AutoFitJson

__author__ = 'amen'
import WebSiteBasePage
import web
import dbconfig
import datamodel.message
import website_config
from webpages.MainPage import pusher
import urllib
import json
import tools.crypt_session

def messag_token(uid):
    return dbconfig.qiniuAuth.upload_token(dbconfig.qiniuSpace,policy={"callbackUrl":'http://%s/upload/MessageDone'%website_config.hostname,
                                                                "callbackBody":'{"name":"$(fname)","hash":"$(etag)","width":"$(imageInfo.width)","height":"$(imageInfo.height)",' +\
                        '"toid":"$(x:toid)","content":"$(x:content)","length":"$(x:length)","uid":%d,"filetype":"$(x:filetype)"}'%uid})
class Message(WebSiteBasePage.AutoPage):
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

        uptoken = messag_token(data['uid'])
        if int(params['usepage'])==0:
            web.header("Content-type","application/json")
            return json.dumps({'token':uptoken})
        tpl=WebSiteBasePage.jinja2_env.get_template('upload/Message.html')
        return tpl.render(token=uptoken)

class MessageDone(WebSiteBasePage.AutoPage):
    def POST(self):
        imgdata=json.loads(web.data())
        with dbconfig.Session() as session:
            newmsg=datamodel.message.Message()
            newmsg.fromid=imgdata['uid']
            newmsg.toid=imgdata['toid']
            content_data=imgdata.get('content')
            if content_data:
                newmsg.content=urllib.unquote_plus(content_data.encode('ascii')).decode('utf-8')
            fileurl=dbconfig.qiniuDownLoadLinkHead+imgdata['hash']
            filetype=int(imgdata['filetype'])
            if filetype==1:
                newmsg.picture=fileurl
                newmsg.width=imgdata['width']
                newmsg.height=imgdata['height']
            elif filetype==2:
                newmsg.voice=fileurl
                newmsg.length=imgdata['length']
            elif filetype==3:
                newmsg.video=fileurl
                newmsg.length=imgdata['length']
            newmsg=session.merge(newmsg)
            session.commit()
            try:
                json_post=json.dumps(newmsg.toJson(),cls=AutoFitJson)
                pusher.rawPush(routing_key='sys.message_to_notify',headers={},body=json_post)
            except Exception,e:
                return json.dumps({'errno':5,'error':str(e)})

            return json.dumps({"errno":0,"error":"Success","result":{"url":fileurl,'msgid':newmsg.msgid}},cls=AutoFitJson)