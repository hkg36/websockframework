from sqlalchemy import and_

from datamodel.connection_info import ConnectionInfo
from datamodel.user import User


__author__ = 'amen'
import random
import dbconfig
import BackEndEnvData

def GenSession(size=15):
    str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    for i in xrange(size):
        str+=chars[random.randint(0, length)]
    return str

def CheckSession(level=0):
    def shell(func):
        def warp(*args,**kwargs):
            with dbconfig.Session() as session:
                cinfo=session.query(ConnectionInfo).filter(and_(ConnectionInfo.connection_id==BackEndEnvData.connection_id,
                                                          ConnectionInfo.queue_id==BackEndEnvData.reply_queue)).first()
                if cinfo is None:
                    return {"errno":1,"error":"session.start not called","result":{}}
                BackEndEnvData.uid=cinfo.uid
                if level>0:
                    uinfo=session.query(User).filter(User.uid==BackEndEnvData.uid).first()
                    if max(uinfo.actor_level,uinfo.active_level)<level:
                        return {"errno":2,"error":"level too low","result":{}}
            result= func(*args,**kwargs)
            BackEndEnvData.uid=None
            return result
        return warp
    return shell
if __name__ == '__main__':
    print GenSession(32)