__author__ = 'amen'
from sqlalchemy import *
import dbconfig
class Post(dbconfig.DBBase):
    __tablename__ = 'post'
    postid=Column(BigInteger,autoincrement=True,primary_key=True,nullable=False)
    uid=Column(BigInteger,nullable=False)
    group_id=Column(BigInteger,default=0)
    text=Column(String(4096))
    picture=Column(String(1024))
    video=Column(String(1024))
    voice=Column(String(1024))
    like=Column(Integer,default=0)
    time=Column(TIMESTAMP,server_default=text('CURRENT_TIMESTAMP'))