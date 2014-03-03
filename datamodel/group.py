#coding:utf-8
__author__ = 'amen'
from sqlalchemy import *

import dbconfig


class Group(dbconfig.DBBase):
    __tablename__ = 'group'
    gid=Column(BigInteger,autoincrement=True,primary_key=True,nullable=False)
    creator=Column(BigInteger,nullable=False,index=True)
    group_name=Column(String(256),nullable=False)
    group_board=Column(String(4096))
    group_postion=Column(String(256))
    type=Column(Integer)
    time=Column(TIMESTAMP,server_default=text('CURRENT_TIMESTAMP'))
    everyone_caninvite=Column(Integer,default=1)
    only_member_speak=Column(Integer,default=0)
    only_member_watch=Column(Integer,default=0)
    geokey=Column(BigInteger,index=True,nullable=False)
    lat=Column(Float,nullable=False)
    long=Column(Float,nullable=False)
    def toJson(self):
        return {'gid':self.gid,
                "creator":self.creator,
                "name":self.group_name,
                "board":self.group_board,
                "type":self.type,
                "position":self.group_postion,
                "time":self.time,
                'everyone_caninvite':self.everyone_caninvite,
                'only_member_speak':self.only_member_speak,
                'only_member_watch':self.only_member_watch,
                'lat':self.lat,
                'long':self.long}

class GroupWatchUpdate(dbconfig.DBBase):
    __tablename__ = 'group_watch'
    uid=Column(BigInteger,primary_key=True,nullable=False,autoincrement=False)
    gid=Column(BigInteger,nullable=False,index=True)