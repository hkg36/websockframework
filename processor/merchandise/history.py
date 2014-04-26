import random
import time
from sqlalchemy import and_
from datamodel.merchandise import StoreMerchandise, StorePayState
from tools.helper import Res
from tools.session import CheckSession

__author__ = 'amen'
import BackEndEnvData
import dbconfig
@CheckSession()
def run(before=None,count=10):
    with dbconfig.Session() as session:
        query=session.query(StorePayState)
        if before:
            query=query.filter(and_(StorePayState.orderid<before,StorePayState.uid==BackEndEnvData.uid))
        else:
            query=query.filter(StorePayState.uid==BackEndEnvData.uid)
        query=query.order_by(StorePayState.orderid.desc()).limit(count)
        pays=query.all()
        paylist=[]
        for pay in pays:
            paylist.append(pay.toJson())
        return Res({'history':paylist})
