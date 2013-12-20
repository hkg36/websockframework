__author__ = 'amen'
from sqlalchemy import *
import dbconfig
class Group(dbconfig.DBBase):
    __tablename__ = 'group'
    gid=Column(BigInteger,autoincrement=True,primary_key=True,nullable=False)
    group_name=Column(String(256),nullable=False)
    group_board=Column(String(4096))
    time=Column(TIMESTAMP,server_default=text('CURRENT_TIMESTAMP'))