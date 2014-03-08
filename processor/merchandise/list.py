#coding:utf-8
from sqlalchemy import and_
from datamodel.merchandise import StoreMerchandise
from tools.helper import Res
from tools.session import CheckSession


__author__ = 'amen'
import BackEndEnvData
import dbconfig
@CheckSession()
def run(gid):
    with dbconfig.Session() as session:
        sm=session.query(StoreMerchandise).filter(and_(StoreMerchandise.group_id==gid,StoreMerchandise.no_list==0)).all()
        smlist=[]
        for one in sm:
            smlist.append(one.toJson())
        return Res({'merchandises':smlist})

