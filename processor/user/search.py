#coding:utf-8
from sqlalchemy import and_
from datamodel.user import User
from tools.helper import Res
from tools.session import CheckSession

__author__ = 'amen'
import dbconfig
import re

@CheckSession()
def run(nick=None):
    if not nick:
        return Res(errno=2,error="no input")
    with dbconfig.Session() as session:
        query=session.query(User)
        if re.match('\d+$',nick):
            query=query.filter(and_(User.phone.like(nick+'%'),User.nick!=None)).order_by(User.nick)
        else:
            query=query.filter(User.nick.like(nick+'%')).order_by(User.nick)
        query=query.limit(20)
        alluser=query.all()
        user_list=[]
        for u in alluser:
            user_list.append({'uid':u.uid,'time':u.create_time})
        return Res({"users":user_list})