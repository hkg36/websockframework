#coding:utf-8
__author__ = 'amen'
from sqlalchemy import *
from mongoengine import *
import dbconfig
import datetime

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

    actor=Column(Integer,default=0)
    actor_level=Column(Integer,default=1)
    active_by=Column(BigInteger,default=0)
    active_level=Column(Integer,default=0)
    active_time=Column(TIMESTAMP)

    is_stew=Column(SmallInteger,default=0)

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
                "create_time":self.create_time,
                'is_stew':self.is_stew,
                }
        if self.active_time:
            data["active_time"]=self.active_time
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
class UserLikeLog(dbconfig.DBBase):
    __tablename__ = 'user_like_log'
    uid=Column(BigInteger,nullable=False)
    by_uid=Column(BigInteger,nullable=False)
    time=Column(TIMESTAMP,server_default=text('CURRENT_TIMESTAMP'))
    __table_args__=(PrimaryKeyConstraint("uid","by_uid"),)

class UserExData(Document):
    uid=LongField(required=True,primary_key=True)
    tags=ListField(StringField(max_length=20))
    position=PointField()
    update_time=DateTimeField()
    like_me_count=LongField(default=0)

    meta = {
        'indexes': ['tags']
    }

    def toJson(self,showpos=False):
        data={"uid":self.uid,"tags":self.tags,"like_me_count":self.like_me_count}
        if showpos and self.position:
            data["lat"]=self.position['coordinates'][1]
            data["long"]=self.position['coordinates'][0]
            data['time']=self.update_time
        return data