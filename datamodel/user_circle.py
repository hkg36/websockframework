#coding:utf-8
__author__ = 'amen'
from sqlalchemy import *
import dbconfig

class CircleDef(dbconfig.DBBase):
    __tablename__ = 'circle_define'
    cid=Column(Integer,nullable=False)
    subid=Column(Integer,nullable=False,default=0)
    level=Column(Integer,nullable=False,default=0)
    title=Column(String(256),nullable=False)

    __table_args__ = (PrimaryKeyConstraint('cid', 'subid'),)

class UserCircle(dbconfig.DBBase):
    __tablename__ = 'user_circle'
    uid=Column(BigInteger,nullable=False)
    cid=Column(Integer,nullable=False)
    subid=Column(Integer,nullable=False,default=0)
    time=Column(TIMESTAMP,server_default=text('CURRENT_TIMESTAMP'))

    __table_args__ = (PrimaryKeyConstraint('uid','cid'),)