#coding:utf-8
from datamodel.connection_info import ConnectionInfo
from datamodel.user import User

__author__ = 'amen'
import BackEndEnvData
import dbconfig
import json
def run(sessionid):
    data=dbconfig.redisdb.get(str('session:%s'%sessionid))
    if data is None:
        return {"errno":1,"error":"session not found","result":{}}
    data=json.loads(data)
    with dbconfig.Session() as session:
        user_data=session.query(User).filter(User.uid==data['uid']).first()
        if user_data:
            session.query(ConnectionInfo).filter(ConnectionInfo.connection_id==BackEndEnvData.connection_id).delete()
            session.commit()
            cinfo=session.query(ConnectionInfo).filter(ConnectionInfo.uid==user_data.uid).first()
            if cinfo is None:
                cinfo=ConnectionInfo()
                cinfo.uid=user_data.uid
            cinfo.connection_id=BackEndEnvData.connection_id
            cinfo.queue_id=BackEndEnvData.reply_queue
            session.merge(cinfo)
            session.commit()
        return {"errno":0,"error":"no error","result":user_data.toJson()}