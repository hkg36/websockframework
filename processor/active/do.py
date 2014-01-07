from datamodel.user import User
from tools.helper import Res
from tools.session import CheckSession

__author__ = 'amen'
import BackEndEnvData
import dbconfig
import datetime

@CheckSession
def run(active_code):
    actinfo=dbconfig.memclient.get(("active_code:%s"%active_code).encode('utf-8'))
    if actinfo is None:
        return Res({},3,"not active code")
    with dbconfig.Session() as session:
        user=session.query(User).filter(User.uid==BackEndEnvData.uid).first()
        user.active_by=actinfo['uid']
        user.active_level=actinfo['level']
        user.active_time=datetime.datetime.now()
        user=session.merge(user)
        session.commit()
        return Res({'active_level':user.actor_level,'active_by':user.active_by})