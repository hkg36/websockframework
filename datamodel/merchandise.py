#coding:utf-8
__author__ = 'amen'
from sqlalchemy import *

import dbconfig


class StoreMerchandise(dbconfig.DBBase):
    __tablename__ = 'store_merchandise'
    mid=Column(BigInteger,autoincrement=True,primary_key=True,nullable=False)
    productcatalog=Column(Integer,default=1)
    productname=Column(String(50),nullable=False)
    productdesc=Column(String(200),nullable=False)
    amount=Column(Integer,default=2)
    time=Column(TIMESTAMP,server_default=text('CURRENT_TIMESTAMP'))

    def toJson(self):
        data={
            'mid':self.mid,
            'productname':self.productname,
            'productdesc':self.productdesc,
            'amount':self.amount,
            'time':self.time
        }
        return data

class StorePayState(dbconfig.DBBase):
    __tablename__ = 'store_paystate'
    orderid=Column(String(64),primary_key=True,nullable=False)
    mid=Column(BigInteger,nullable=False)
    uid=Column(BigInteger,nullable=False)
    paystate=Column(Integer,default=0)
    create_time=Column(TIMESTAMP,server_default=text('CURRENT_TIMESTAMP'))
    paytime=Column(TIMESTAMP)
    refundtime=Column(TIMESTAMP)
