#coding:utf-8
__author__ = 'amen'
from sqlalchemy import *
import dbconfig
class PostReply(dbconfig.DBBase):
    __tablename__ = 'post_reply'
    replyid=Column(BigInteger,autoincrement=True,primary_key=True,nullable=False)
    postid=Column(BigInteger,nullable=False)
    uid=Column(BigInteger,nullable=False)
    content=Column(String(4096))
    like=Column(Integer,default=0)
    time=Column(TIMESTAMP,server_default=text('CURRENT_TIMESTAMP'))

    def toJson(reply):
        return {
            "replyid":reply.replyid,
            "postid":reply.postid,
            "uid":reply.uid,
            "content":reply.content,
            "time":reply.time
        }