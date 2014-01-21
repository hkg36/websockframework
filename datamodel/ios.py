#coding:utf-8
__author__ = 'amen'
from sqlalchemy import *
import dbconfig
import time
class IOSDevice(dbconfig.DBBase):
    __tablename__ = 'iosdevice'
    uid=Column(BigInteger,primary_key=True,nullable=False)
    device_token=Column(String(256),nullable=False)
    is_debug=Column(SmallInteger,nullable=False,default=0)
    time=Column(TIMESTAMP,server_default=text('CURRENT_TIMESTAMP'))