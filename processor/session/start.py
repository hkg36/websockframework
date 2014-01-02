from datamodel.connection_info import ConnectionInfo
from datamodel.user import User

__author__ = 'amen'
import BackEndEnvData
import dbconfig
import anyjson
def run(sessionid):
    data=dbconfig.memclient.get(str('session:%s'%sessionid))
    if data is None:
        return {"errno":1,"error":"session not found","result":{}}
    session=dbconfig.Session()
    user_data=session.query(User).filter(User.uid==data['uid']).first()
    if user_data:
        cinfo=ConnectionInfo()
        cinfo.uid=user_data.uid
        cinfo.connection_id=BackEndEnvData.connection_id
        cinfo.queue_id=BackEndEnvData.reply_queue
        session.merge(cinfo)
    user_json=user_data.toJson()
    session.commit()
    session.close()
    return {"errno":0,"error":"no error","result":user_json}