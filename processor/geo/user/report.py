#coding:utf-8
from datamodel.user_geo_position import UserGeoPosition
from tools.helper import Res, CombineGeo
from tools.session import CheckSession

__author__ = 'amen'
import BackEndEnvData
import dbconfig

@CheckSession
def run(long,lat):
    with dbconfig.Session() as session:
        userpos=UserGeoPosition()
        userpos.uid=BackEndEnvData.uid
        userpos.long=long
        userpos.lat=lat
        userpos.geokey=CombineGeo(long,lat)
        session.merge(userpos)
        session.commit()
    return Res()