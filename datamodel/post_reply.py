__author__ = 'amen'
from sqlalchemy import *
import dbconfig
class PostReply(dbconfig.DBBase):
    __tablename__ = 'post_reply'
    replyid=Column(BigInteger,autoincrement=True,primary_key=True,nullable=False)
    postid=Column(BigInteger,nullable=False)
    uid=Column(BigInteger,nullable=False)
    text=Column(String(4096))
    like=Column(Integer,default=0)