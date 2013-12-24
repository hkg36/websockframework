from sqlalchemy import and_
from datamodel.connection_info import ConnectionInfo

__author__ = 'amen'
import random
import dbconfig
import BackEndEnvData

def GenSession():
    str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    for i in xrange(15):
        str+=chars[random.randint(0, length)]
    return str

def CheckSession(func):
    def warp(*args,**kwargs):
        session=dbconfig.Session()
        cinfo=session.query(ConnectionInfo).filter(and_(ConnectionInfo.connection_id==BackEndEnvData.connection_id,
                                                  ConnectionInfo.queue_id==BackEndEnvData.reply_queue)).first()
        if cinfo is None:
            return {"errno":1,"error":"session not found","result":{}}
        BackEndEnvData.uid=cinfo.uid
        result= func(*args,**kwargs)
        BackEndEnvData.uid=None
        return result
    return warp