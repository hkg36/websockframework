#coding:utf-8
from datamodel.merchandise import StoreMerchandise, StoreGroup
from tools.helper import Res
from tools.session import CheckSession


__author__ = 'amen'
import BackEndEnvData
import dbconfig
@CheckSession()
def run():
    with dbconfig.Session() as session:
        groups=session.query(StoreGroup).all()
        grouplist=[]
        for g in groups:
            grouplist.append(g.toJson())
        return Res({'groups':grouplist})
