#coding:utf-8
__author__ = 'amen'
from sqlalchemy import *

import dbconfig


class User(dbconfig.DBBase):
    __tablename__ = 'user'
    uid=Column(BigInteger,autoincrement=True,primary_key=True,nullable=False)
    phone=Column(String(40),unique=True,nullable=False)
    nick=Column(String(32),index=True)
    signature=Column(String(512))
    password=Column(String(128))
    headpic=Column(String(1024))
    sex=Column(Integer,default=0)
    birthday = Column(DateTime)
    marriage = Column(Integer)
    background_image = Column(String(1024))
    height = Column(Integer, default=0)
    position = Column(String(256))
    tags=Column(String(512))

    actor=Column(Integer,default=0)
    actor_level=Column(Integer,default=1)
    active_by=Column(BigInteger,default=0)
    active_level=Column(Integer,default=0)
    active_time=Column(TIMESTAMP)

    create_time=Column(TIMESTAMP,server_default=text('CURRENT_TIMESTAMP'))
    def toJson(self,showphone=False):
        data = {"uid":self.uid,
                "nick":self.nick,
                "signature":self.signature,
                "headpic":self.headpic,
                "sex":self.sex,
                "birthday":self.birthday,
                "marriage":self.marriage,
                "background_image":self.background_image,
                "height":self.height,
                "position":self.position,
                "actor":self.actor,
                "actor_level":self.actor_level,
                "active_by":self.active_by,
                "active_level":self.active_level,
                "create_time":self.create_time}
        if self.active_time:
            data["active_time"]=self.active_time
        if self.tags:
            data["tags"]=self.tags.split('|')
        if showphone:
            data['phone']=self.phone
        return data
class UserExMedia(dbconfig.DBBase):
    __tablename__ = 'user_ex_media'
    did=Column(BigInteger,autoincrement=True,primary_key=True,nullable=False)
    uid=Column(BigInteger,index=True,nullable=False)
    picture=Column(String(1024))
    video=Column(String(1024))
    voice=Column(String(1024))
    width=Column(Integer)
    height=Column(Integer)
    length=Column(Integer)
    time=Column(TIMESTAMP,server_default=text('CURRENT_TIMESTAMP'))
    text=Column(String(256))

    def toJson(self):
        data={'did':self.did,
              'uid':self.uid,
              'text':self.text,
              'time':self.time}
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