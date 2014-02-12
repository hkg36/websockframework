#coding:utf-8
__author__ = 'amen'
from sqlalchemy import *

import dbconfig


class UserGeoPosition(dbconfig.DBBase):
    __tablename__ = 'user_geo_pos'
    uid=Column(BigInteger,autoincrement=True,primary_key=True,nullable=False)
    geokey=Column(BigInteger,index=True,nullable=False)
    lat=Column(Float,nullable=False)
    long=Column(Float,nullable=False)
    time=Column(TIMESTAMP,server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))

    def toJson(self):
        return {"uid":self.uid,
                "lat":self.lat,
                "long":self.long,
                "time":self.time}