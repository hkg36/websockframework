#coding:utf-8
from datamodel.user import UserExData
from datamodel.user_geo_position import UserGeoPosition
from tools.helper import Res, CombineGeo
from tools.session import CheckSession

__author__ = 'amen'
import BackEndEnvData
import dbconfig
import datetime

@CheckSession()
def run(long,lat):
    with dbconfig.Session() as session:
        exdata=UserExData.objects(uid=BackEndEnvData.uid).first()
        if exdata is None:
            exdata=UserExData(uid=BackEndEnvData.uid)
        exdata.position=[long,lat]
        exdata.update_time=datetime.datetime.now()
        exdata.save()
    return Res()