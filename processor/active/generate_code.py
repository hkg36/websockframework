#coding:utf-8
from datamodel.user import User
from tools.helper import Res
from tools.session import CheckSession, GenSession

__author__ = 'amen'
import BackEndEnvData
import dbconfig

@CheckSession
def run(level=1):
    with dbconfig.Session() as session:
        user_info=session.query(User).filter(User.uid==BackEndEnvData.uid).first()
        if user_info.actor==0:
            return Res({},2,'not a actor')
        if user_info.actor_level<level:
            return Res({},2,'not enough level')
        act_code=GenSession()
        dbconfig.memclient.set("active_code:%s"%act_code,{'uid':BackEndEnvData.uid,'level':level},time=20*60)
        return Res({'active_code':act_code,'level':level})