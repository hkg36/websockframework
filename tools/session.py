from sqlalchemy import and_

from datamodel.connection_info import ConnectionInfo
from datamodel.user import User
from tools.helper import Res


__author__ = 'amen'
import random
import dbconfig
import BackEndEnvData
import urllib

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
                if BackEndEnvData.uid is None:
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
def FrequencyControl(time_sec=10):
    def ACF(fun):
        def Work(*args,**kwargs):
            fkey= 'funFreqCtrl:%s.%s[%d]'%(fun.__module__,fun.__name__,BackEndEnvData.uid)
            fkey=urllib.quote(fkey)
            if dbconfig.memclient.add(fkey,'1',time=time_sec):
                return fun(*args,**kwargs)
            else:
                return Res(errno=4,error='too quick,stop!!!')
        return Work
    return ACF
if __name__ == '__main__':
    print GenSession(32)