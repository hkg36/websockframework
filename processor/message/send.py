#coding:utf-8
from datamodel.message import Message
from tools.addPushQueue import AddMessageTrans
from tools.helper import Res
from tools.session import CheckSession

__author__ = 'amen'
import BackEndEnvData
import dbconfig
@CheckSession()
def run(uid,content=None,lat=None,long=None,picture=None):
    if content==None and (lat==None or long==None) and picture==None:
        return Res(errno=3,error="param error")
    with dbconfig.Session() as session:
        newmsg=Message()
        newmsg.toid=uid
        newmsg.fromid=BackEndEnvData.uid
        newmsg.content=content
        newmsg.lat=lat
        newmsg.long=long
        newmsg.picture=picture
        newmsg=session.merge(newmsg)
        session.commit()
        AddMessageTrans(newmsg.toJson())
        return Res({'msgid':newmsg.msgid})