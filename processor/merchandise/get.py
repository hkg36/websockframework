#coding:utf-8
from sqlalchemy import and_
from datamodel.merchandise import StoreMerchandise
from tools.helper import Res
from tools.session import CheckSession


__author__ = 'amen'
import BackEndEnvData
import dbconfig
@CheckSession()
def run(mid):
    if isinstance(mid,list)==False:
        mid=[mid]
    with dbconfig.Session() as session:
        sms=session.query(StoreMerchandise).filter(StoreMerchandise.mid.in_(mid)).all()
        smlist=[]
        for sm in sms:
            smlist.append(sm.toJson())
        return Res({'merchandises':smlist})
