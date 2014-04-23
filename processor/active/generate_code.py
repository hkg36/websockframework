#coding:utf-8
from datamodel.user import User
from tools.helper import Res
from tools.session import CheckSession, GenSession

__author__ = 'amen'
import BackEndEnvData
import dbconfig
import time

TIMEOUT=45*60
@CheckSession()
def run(level=1):
    if level==0:
        return Res(errno=2,error="can not set level to 0")
    with dbconfig.Session() as session:
        user_info=session.query(User).filter(User.uid==BackEndEnvData.uid).first()
        if user_info.actor==0:
            return Res({},2,'not a actor')
        if user_info.actor_level<level:
            return Res({},2,'not enough level')
        act_code=GenSession(8)
        dbconfig.memclient.set("active_code:%s"%act_code,{'uid':BackEndEnvData.uid,'level':int(level)},time=TIMEOUT)
        return Res({'active_code':act_code,'level':level,'timeout':time.time()+TIMEOUT})