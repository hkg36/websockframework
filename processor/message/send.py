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
    newmsg_id=newmsg.msgid
    newmsg_json=newmsg.toJson()
    session.commit()
    session.close()
    AddMessageTrans(newmsg_json)
    return Res({'msgid':newmsg_id})