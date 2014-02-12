#coding:utf-8
from sqlalchemy import and_

from datamodel.message import Message
from tools.helper import Res
from tools.session import CheckSession


__author__ = 'amen'
import BackEndEnvData
import dbconfig
@CheckSession()
def run(afterid=0):
    with dbconfig.Session() as session:
        if afterid==0:
            query=session.query(Message).filter(Message.toid==BackEndEnvData.uid).order_by(Message.msgid.desc()).limit(100)
        else:
            query=session.query(Message).filter(and_(Message.toid==BackEndEnvData.uid,Message.msgid>afterid))\
                .order_by(Message.msgid.desc()).limit(100)
        msgs=query.all()
        msglist=[]
        for msg in msgs:
            msglist.append(msg.toJson())
        return Res({'message':msglist})