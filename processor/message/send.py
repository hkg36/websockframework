from datamodel.message import Message
from tools.addPushQueue import AddMessageTrans
from tools.helper import Res
from tools.session import CheckSession

__author__ = 'amen'
import BackEndEnvData
import dbconfig
@CheckSession
def run(uid,content):
    with dbconfig.Session() as session:
        newmsg=Message()
        newmsg.toid=uid
        newmsg.fromid=BackEndEnvData.uid
        newmsg.content=content
        newmsg=session.merge(newmsg)
        session.commit()
        AddMessageTrans(newmsg.toJson())
        return Res({'msgid':newmsg.msgid})