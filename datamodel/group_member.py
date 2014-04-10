#coding:utf-8
__author__ = 'amen'
from sqlalchemy import *

import dbconfig


class GroupMember(dbconfig.DBBase):
    __tablename__ = 'group_member'
    gid=Column(BigInteger,nullable=False)
    uid=Column(BigInteger,nullable=False)
    type=Column(Integer,default=0) #添加途径
    time=Column(TIMESTAMP,server_default=text('CURRENT_TIMESTAMP'))
    can_post=Column(SmallInteger,default=1)

    __table_args__ = (PrimaryKeyConstraint('gid', 'uid', name='goupuser_uc'),)

    def toJson(self):
        return {'uid':self.uid,"type":self.type,"time":self.time,"can_post":self.can_post}