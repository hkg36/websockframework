#coding:utf-8
from sqlalchemy import between, and_
from datamodel.user_geo_position import UserGeoPosition
from tools.helper import Res, CombineGeo
from tools.session import CheckSession

__author__ = 'amen'
import BackEndEnvData
import dbconfig

SEARCH_R=0.03
@CheckSession
def run(long,lat):
    lat_min=lat-SEARCH_R
    lat_max=lat+SEARCH_R
    long_min=long-SEARCH_R
    long_max=long+SEARCH_R
    geokey_min=CombineGeo(long_min,lat_min)
    geokey_max=CombineGeo(long_max,lat_max)
    with dbconfig.Session() as session:
        users=session.query(UserGeoPosition).filter(
         and_(
         between(UserGeoPosition.geokey,geokey_min,geokey_max),
         between(UserGeoPosition.lat,lat_min,lat_max),
         between(UserGeoPosition.long,long_min,long_max)
        )
        ).all()
        ulist=[]
        for user in users:
            ulist.append(user.toJson())
        return Res({"users":ulist})