import random
import time
from sqlalchemy import and_
from datamodel.tenpaylog import TenpayState
from tools.helper import Res
from tools.session import CheckSession

__author__ = 'amen'
import BackEndEnvData
import dbconfig
@CheckSession()
def run(before=None,count=10):
    query={"uid":BackEndEnvData.uid,"paystate__ne":0}
    if before:
        query['orderid__lt']=before
    ts_all=TenpayState.objects(**query).order_by('-orderid').limit(int(count))
    tslist=[]
    for one in ts_all:
        tslist.append(one.toJson())
    return Res({'history':tslist})