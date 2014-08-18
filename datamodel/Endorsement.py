#coding:utf-8
import dbconfig

__author__ = 'amen'
from sqlalchemy import *

class Endorsement(dbconfig.DBBase):
    __tablename__ = 'user_endorsement'
    uid=Column(BigInteger,nullable=False)
    mid=Column(BigInteger,nullable=False)
    slogan=Column(String(512))
    create_time=Column(TIMESTAMP,server_default=text('CURRENT_TIMESTAMP'))

    __table_args__ = (PrimaryKeyConstraint('uid', 'mid'),)

    def toJson(self):
        data={
            "uid":self.uid,
            "mid":self.mid,
            "slogan":self.slogan,
            "create_time":self.create_time
        }
        return data

class EndorsementInfo(dbconfig.DBBase):
    __tablename__ = 'user_endorsement_info'
    uid=Column(BigInteger,nullable=False,primary_key=True)
    endorsement_type=Column(Integer,default=0)
    endorsement_point=Column(BigInteger,default=0)
    consumer_point=Column(BigInteger,default=0)
    level=Column(Integer,default=0)
    type=Column(String(32))
    order_weigth=Column(Integer,default=0)
    create_time=Column(TIMESTAMP,server_default=text('CURRENT_TIMESTAMP'))

    def toJson(self):
        data={'endorsement_point':self.endorsement_point,
              'endorsement_type':self.endorsement_type,
              'consumer_point':self.consumer_point,
              'level':self.level,
                "create_time":self.create_time}
        if self.type:
            data['type']=self.type.split(',')
        return data

