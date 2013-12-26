from datamodel.message import Message
from tools.addPushQueue import AddMessageTrans
from tools.helper import Res
from tools.session import CheckSession

__author__ = 'amen'
import BackEndEnvData
import dbconfig
@CheckSession
def run(uid,content):
    session=dbconfig.Session()
    newmsg=Message()
    newmsg.toid=uid
    newmsg.fromid=BackEndEnvData.uid
    newmsg.content=content
    newmsg=session.merge(newmsg)
    session.flush()
    session.commit()
    AddMessageTrans(newmsg)
    return Res({'msgid':newmsg.msgid})