#coding:utf-8
__author__ = 'amen'
from sqlalchemy import *
import dbconfig
import time
class PhoneBook(dbconfig.DBBase):
    __tablename__='phone_book'
    uid=Column(BigInteger,nullable=False)
    phone=Column(String(32),nullable=False,index=True)
    name=Column(String(32))

    __table_args__ = (PrimaryKeyConstraint('uid', 'phone'),)