#coding:utf-8
from datamodel.user import UserExData
from tools.helper import Res, CombineGeo
from tools.session import CheckSession

__author__ = 'amen'
import BackEndEnvData
import dbconfig
import datetime

@CheckSession()
def run(long,lat):
    UserExData.objects(uid=BackEndEnvData.uid).update_one(upsert=True,set__position=[long,lat],set__update_time=datetime.datetime.now())
    return Res()