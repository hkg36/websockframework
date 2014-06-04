#coding:utf-8
from datamodel.user import User, UserExData
from tools.helper import Res
from tools.session import CheckSession

__author__ = 'amen'
import BackEndEnvData
import dbconfig


@CheckSession()
def run(nick=None,signature=None, sex=None, birthday=None, marriage=None, height=None,position=None,
        tags=None,headpic=None):
    with dbconfig.Session() as session:
        if nick:
            user=session.query(User).filter(User.nick==nick).first()
            if user:
                if user.uid!=BackEndEnvData.uid:
                    return Res(errno=1000,error="nick be taken")
        user=session.query(User).filter(User.uid==BackEndEnvData.uid).first();
        if user is None:
            return Res(errno=3,error='data error')
        if nick:
            user.nick=nick
        if signature:
            user.signature=signature
        if sex:
            user.sex=sex
        if birthday:
            user.birthday=birthday
        if marriage:
            user.marriage=marriage
        if height:
            user.height=height
        if position:
            user.position=position
        if headpic:
            user.headpic=headpic
        session.merge(user)
        session.commit()
    return Res()