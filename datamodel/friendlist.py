#coding:utf-8
__author__ = 'amen'
from sqlalchemy import *
import dbconfig
class FriendList(dbconfig.DBBase):
    __tablename__ = 'friendlist'
    uid=Column(BigInteger,nullable=False)
    friendid=Column(BigInteger,nullable=False,index=True)
    type=Column(Integer,default=0) #添加途径
    time=Column(TIMESTAMP,server_default=text('CURRENT_TIMESTAMP'))

    __table_args__ = (PrimaryKeyConstraint('uid', 'friendid', name='friendid_uc'),
    {'mysql_engine':'MyISAM'})