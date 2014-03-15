#coding:utf-8
from sqlalchemy import between, and_
from datamodel.user import UserExData

from datamodel.user_geo_position import UserGeoPosition
from tools.helper import Res, CombineGeo
from tools.session import CheckSession


__author__ = 'amen'
import dbconfig

SEARCH_R=0.03
@CheckSession()
def run(long,lat):
    with dbconfig.Session() as session:
        ulist=[]

        for user in UserExData.objects(position__geo_within_sphere=[(long,lat),SEARCH_R]).only('uid','position','update_time'):
            ulist.append({"uid":user.uid,
                "lat":user.position['coordinates'][1],
                "long":user.position['coordinates'][0],
                "time":user.update_time})
        return Res({"users":ulist})