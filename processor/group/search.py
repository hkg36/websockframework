#coding:utf-8
from datamodel.group import Group
from tools.helper import Res
from tools.session import CheckSession

__author__ = 'amen'
import BackEndEnvData
import dbconfig


@CheckSession()
def run(type):
    with dbconfig.Session() as session:
        gms=session.query(Group).filter(Group.type==type).limit(100).all()
        glist=[]
        for gm in gms:
            glist.append(gm.toJson())
        return Res({'groups':glist})