#coding:utf-8
from sqlalchemy import text, or_
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
            session.execute(text('delete from connection_info where uid=:uid or (queue_id=:queue_id and connection_id=:connection_id)'),
                            {"uid":user_data.uid,"queue_id":BackEndEnvData.reply_queue,"connection_id":BackEndEnvData.connection_id})
            session.execute(
                text('insert into connection_info(uid,queue_id,connection_id) values(:uid,:queue_id,:connection_id) ON DUPLICATE KEY UPDATE queue_id=:queue_id,connection_id=:connection_id'),
                {"uid":user_data.uid,"queue_id":BackEndEnvData.reply_queue,"connection_id":BackEndEnvData.connection_id})
            session.commit()
        return {"errno":0,"error":"no error","result":user_data.toJson()}