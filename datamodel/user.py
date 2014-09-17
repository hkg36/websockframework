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
    birthday = Column(Integer)
    marriage = Column(Integer)
    background_image = Column(String(1024))
    height = Column(Integer, default=0)
    position = Column(String(256))
    job=Column(String(32))

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
                "job":self.job,
                }
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
    client_data=DictField()

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

class UserInviteLog(Document):
    invite_id=SequenceField(primary_key=True)
    uid=LongField(required=True)
    phone=StringField(required=True)
    headpic=URLField()
    sex=IntField()
    nick=StringField(max_length=32)
    birthday = DateTimeField()
    marriage = IntField(default=0)
    height = IntField(default=0)
    join_cid=IntField()
    join_roleid=IntField()
    position = StringField(max_length=256)
    joined_uid=LongField()
    create_time=DateTimeField(default=datetime.datetime.now)
    sms_send_time=DateTimeField()

    meta = {
        'indexes': [{'fields':('uid','phone'), 'unique': True},'phone']
    }

    def toJson(self):
        data={
            'invite_id':self.invite_id,
            'uid':self.uid,
            'phone':self.phone,
            'headpic':self.headpic,
            'sex':self.sex,
            'nick':self.nick,
            'birthday':self.birthday,
            'marriage':self.marriage,
            'height':self.height,
            'join_cid':self.join_cid,
            'join_roleid':self.join_roleid,
            'position':self.position,
            'joined_uid':self.joined_uid,
            'create_time':self.create_time,
            'sms_send_time':self.sms_send_time
        }
        return data

class UserPostAddress(dbconfig.DBBase):
    __tablename__ = 'user_post_address'
    addrid=Column(BigInteger,autoincrement=True,primary_key=True,nullable=False)
    uid=Column(BigInteger,index=True)
    province=Column(String(32))
    city=Column(String(32))
    zone=Column(String(32))
    detail=Column(String(256))
    phone=Column(String(16))
    name=Column(String(16))
    use_time=Column(Integer)

    def toJson(self):
        data={'addrid':self.addrid,
              'uid':self.uid,
              'province':self.province,
              'city':self.city,
              'zone':self.zone,
              'detail':self.detail,
              'phone':self.phone,
              'name':self.name,
              'use_time':self.use_time}
        return data