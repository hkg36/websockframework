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
    ex_people_amount=Column(Integer,default=0)
    time=Column(TIMESTAMP,server_default=text('CURRENT_TIMESTAMP'))

    def toJson(self):
        data={
            'mid':self.mid,
            'productname':self.productname,
            'productdesc':self.productdesc,
            'amount':self.amount,
            'time':self.time,
            'ex_people_amount':self.ex_people_amount
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
    yborderid=Column(String(64))
    remain=Column(Integer)
    ex_people=Column(Integer)

class StorePayLog(dbconfig.DBBase):
    __tablename__ = 'store_paylog'
    payid=Column(BigInteger,autoincrement=True,primary_key=True,nullable=False)
    orderid=Column(String(64),nullable=False)
    mid=Column(BigInteger,nullable=False)
    uid=Column(BigInteger,nullable=False)
    paystate=Column(Integer,default=0)
    productcatalog=Column(Integer,default=1)
    productname=Column(String(50),nullable=False)
    productdesc=Column(String(200),nullable=False)
    amount=Column(Integer,default=2)
    ex_people=Column(Integer)
    create_time=Column(TIMESTAMP,server_default=text('CURRENT_TIMESTAMP'))

    def __init__(self,Merchandise,PayState):
        super(StorePayLog,self).__init__()
        self.orderid=PayState.orderid
        self.mid=PayState.mid
        self.uid=PayState.uid
        self.paystate=PayState.paystate
        self.productcatalog=Merchandise.productcatalog
        self.productname=Merchandise.productname
        self.productdesc=Merchandise.productdesc
        self.amount=PayState.amount
        self.ex_people=PayState.ex_people

    def toJson(self):
        data={
            'payid':self.payid,
            'mid':self.mid,
            'uid':self.uid,
            'paystate':self.paystate,
            'productcatalog':self.productcatalog,
            'productname':self.productname,
            'productdesc':self.productdesc,
            'amount':self.amount,
            'create_time':self.create_time,
            'ex_people':self.ex_people
        }
        return data
