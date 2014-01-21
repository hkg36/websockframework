#coding:utf-8
from datamodel.user import User
from tools.helper import Res
from tools.session import CheckSession

__author__ = 'amen'
import BackEndEnvData
import dbconfig
import anyjson
@CheckSession
def run(nick=None):
    with dbconfig.Session() as session:
        query=session.query(User)
        if nick:
            query=query.filter(User.nick.like(nick+'%')).order_by(User.nick)
        query=query.limit(20)
        alluser=query.all()
        user_list=[]
        for u in alluser:
            user_list.append(u.toJson())
    return Res({"users":user_list})