#coding:utf-8
__author__ = 'amen'
from sqlalchemy import *

import dbconfig


class Post(dbconfig.DBBase):
    __tablename__ = 'post'
    postid=Column(BigInteger,autoincrement=True,primary_key=True,nullable=False)
    uid=Column(BigInteger,nullable=False,index=True)
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
    excount=Column(Integer,default=0)
    time=Column(TIMESTAMP,server_default=text('CURRENT_TIMESTAMP'))
    def toJson(post):
        data= {'postid':post.postid,
                'uid':post.uid,
                'gid':post.group_id,
                'like':post.like,
                'replycount':post.replycount,
                'excount':post.excount,
                'time':post.time
                }
        data['content']=post.content
        if post.picture:
            data['type']='pic'
            data['picture']=post.picture
            data['width']=post.width
            data['height']=post.height
        elif post.video:
            data['type']='vdo'
            data['video']=post.video
            data['length']=post.length
        elif post.voice:
            data['type']="vic"
            data['voice']=post.voice
            data['length']=post.length
        return data
class PostExData(dbconfig.DBBase):
    __tablename__ = 'post_ex_data'
    did=Column(BigInteger,autoincrement=True,primary_key=True,nullable=False)
    postid=Column(BigInteger,index=True,nullable=False)
    picture=Column(String(1024))
    video=Column(String(1024))
    voice=Column(String(1024))
    width=Column(Integer)
    height=Column(Integer)
    length=Column(Integer)
    def toJson(self):
        data={'did':self.did,
              'postid':self.postid}
        if self.picture:
            data['type']='pic'
            data['picture']=self.picture
            data['width']=self.width
            data['height']=self.height
        elif self.video:
            data['type']='vdo'
            data['video']=self.video
            data['length']=self.length
        elif self.voice:
            data['type']="vic"
            data['voice']=self.voice
            data['length']=self.length
        return data