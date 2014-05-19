#coding:utf-8
from sqlalchemy import and_
import WebSiteBasePage
import web
from datamodel.message import Message
from datamodel.user_circle import CircleDef, CircleBoardHistory, UserCircle
import dbconfig
from tools.helper import DefJsonEncoder
from webpages.MainPage import pusher

__author__ = 'amen'
class UpdateCircleBoard(WebSiteBasePage.AutoPage):
    def GET(self):
        tpl=WebSiteBasePage.jinja2_env.get_template('operational/update_circle_board.html')
        return tpl.render()
    def POST(self):
        params=web.input()
        cid=int(params.get('cid'))
        board=params.get('board')
        with dbconfig.Session() as session:
            cdef=session.query(CircleDef).filter(CircleDef.cid==cid).first()
            cdef.board=board
            cdef=session.merge(cdef)
            cbhistory=CircleBoardHistory()
            cbhistory.cid=cid
            cbhistory.board=board
            cbhistory=session.merge(cbhistory)
            session.commit()
            pusher.rawPush(routing_key="sys.circle_new_board",headers={"type":"circle.newboard"},body=DefJsonEncoder.encode(cbhistory.toJson()))
        return DefJsonEncoder.encode({"cid":cid,"board":board})

class SendMessageToCircleUser(WebSiteBasePage.AutoPage):
    def GET(self):
        tpl=WebSiteBasePage.jinja2_env.get_template('operational/send_message_to_circle_user.html')
        return tpl.render()
    def POST(self):
        params=web.input()
        cid=int(params.get('cid'))
        from_uid=int(params.get("from_uid",1))
        roleids=[int(one) for one in params.get('roleid',"0").split(',')]
        if not cid:
            return 'need cid'
        content=params.get('content')
        if not content:
            return 'need content'

        with dbconfig.Session() as session:
            query_params=UserCircle.cid==cid
            if len(roleids)>0 and 0 not in roleids:
                query_params=and_(query_params,UserCircle.roleid.in_(roleids))
            allUser=session.query(UserCircle).filter(query_params).all()
            alluid=[one.uid for one in allUser]
            newmsgs=[]
            for to_uid in alluid:
                newmsg=Message()
                newmsg.toid=to_uid
                newmsg.fromid=from_uid
                newmsg.content=content
                newmsg=session.merge(newmsg)
                newmsgs.append(newmsg)
            session.commit()
            msgids=[]
            for newmsg in newmsgs:
                msgids.append(newmsg.msgid)
                json_msg=DefJsonEncoder.encode(newmsg.toJson())
                pusher.rawPush(body=json_msg,headers={},
                                                    routing_key='sys.message_to_notify')

            return DefJsonEncoder.encode({'msgid':msgids})