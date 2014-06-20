#coding:utf-8
import WebSiteBasePage
import web
from datamodel.message import Message
import dbconfig
from tools.helper import DefJsonEncoder, DecodeCryptSession
from webpages.MainPage import pusher
from webpages.operational_background.obtools import AccessControl

__author__ = 'amen'
class SendMessageToUser(WebSiteBasePage.AutoPage):
    def GET(self):
        tpl=WebSiteBasePage.jinja2_env.get_template('operational/send_message_to_user.html')
        return tpl.render()
    def POST(self):
        params=web.input(from_uid=1)
        from_uid=int(params.get('from_uid',1))
        to_uid=int(params.get('to_uid',0))
        if not to_uid:
            return 'need to_uid'
        content=params.get('content')
        if not content:
            return 'need content'

        with dbconfig.Session() as session:
            newmsg=Message()
            newmsg.toid=to_uid
            newmsg.fromid=from_uid
            newmsg.content=content
            newmsg=session.merge(newmsg)
            session.commit()

            json_msg=DefJsonEncoder.encode(newmsg.toJson())
            pusher.rawPush(body=json_msg,headers={},
                                                routing_key='sys.message_to_notify')
            return DefJsonEncoder.encode({'msgid':newmsg.msgid})

class FindSession(WebSiteBasePage.AutoPage):
    def GET(self):
        params=web.input()
        sessionid=params['sessionid']
        uiddata=DecodeCryptSession(sessionid)
        if uiddata:
            return DefJsonEncoder.encode(uiddata)
        return dbconfig.redisdb.get('session:'+params['sessionid'])
    def POST(self):
        return self.GET()


