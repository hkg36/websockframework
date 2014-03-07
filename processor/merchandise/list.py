#coding:utf-8
from datamodel.merchandise import StoreMerchandise
from tools.helper import Res
from tools.session import CheckSession


__author__ = 'amen'
import BackEndEnvData
import dbconfig
@CheckSession()
def run(gid):
    with dbconfig.Session() as session:
        sm=session.query(StoreMerchandise).filter(StoreMerchandise.group_id==gid).all()
        smlist=[]
        for one in sm:
            smlist.append(one.toJson())
        return Res({'merchandises':smlist})

