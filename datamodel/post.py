__author__ = 'amen'
from sqlalchemy import *
import dbconfig
import time
class Post(dbconfig.DBBase):
    __tablename__ = 'post'
    postid=Column(BigInteger,autoincrement=True,primary_key=True,nullable=False)
    uid=Column(BigInteger,nullable=False)
    group_id=Column(BigInteger,default=0)
    content=Column(String(4096))
    picture=Column(String(1024))
    video=Column(String(1024))
    voice=Column(String(1024))
    width=Column(Integer)
    height=Column(Integer)
    length=Column(Integer)
    like=Column(Integer,default=0)
    replycount=Column(Integer,default=0)
    time=Column(TIMESTAMP,server_default=text('CURRENT_TIMESTAMP'))

    def toJson(post):
        data= {'postid':post.postid,
                'uid':post.uid,
                'gid':post.group_id,
                'content':post.content,
                'like':post.like,
                'replycount':post.replycount,
                'time':time.mktime(post.time.timetuple())
                }
        if post.picture:
            data['picture']=post.picture
            data['width']=post.width
            data['height']=post.height
        if post.video:
            data['video']=post.video
            data['length']=post.length
        if post.voice:
            data['voice']=post.voice
            data['length']=post.length
        return data