#coding:utf-8
__author__ = 'amen'
from sqlalchemy import *

import dbconfig

class RecommendUser(dbconfig.DBBase):
    __tablename__ = 'recommend_user'
    uid=Column(BigInteger,nullable=False)
    recommend_uid=Column(BigInteger,nullable=False,index=True)
    recommend_word=Column(String(1024),nullable=False)
    city=Column(String(32),nullable=False)
    sex=Column(Integer,nullable=False)
    sex_want=Column(Integer,nullable=False,default=0)
    contact=Column(String(256),nullable=False)
    message_count=Column(Integer,default=0)
    like_count=Column(Integer,default=0)
    buy_count=Column(Integer,default=0)
    media_count=Column(Integer,default=0)
    age=Column(String(32))
    create_time=Column(TIMESTAMP,server_default=text('CURRENT_TIMESTAMP'))
    tags=Column(String(512))

    __table_args__=(PrimaryKeyConstraint("uid","recommend_uid"),)

    def toJson(self,show_all=False):
        data={'uid':self.uid,
              "recommend_uid":self.recommend_uid,
              "recommend_word":self.recommend_word,
              "city":self.city,
              "sex":self.sex,
              "sex_want":self.sex_want,
              "message_count":self.message_count,
              "like_count":self.like_count,
              "buy_count":self.buy_count,
              "media_count":self.media_count,
              "create_time":self.create_time,
              "age":self.age,

              }
        if self.tags:
            data["tags"]=self.tags.split('|')
        if show_all:
            data["contact"]=self.contact
        return data

Index('recommend_city_user_sex_want_index',RecommendUser.city,
      RecommendUser.sex,RecommendUser.sex_want)

class RecommendMedia(dbconfig.DBBase):
    __tablename__ = 'recommend_media'
    did=Column(BigInteger,autoincrement=True,primary_key=True,nullable=False)
    uid=Column(BigInteger,nullable=False)
    recommend_uid=Column(BigInteger,nullable=False)
    picture=Column(String(1024))
    video=Column(String(1024))
    voice=Column(String(1024))
    width=Column(Integer)
    height=Column(Integer)
    length=Column(Integer)
    def toJson(self):
        data={'did':self.did,
              'uid':self.uid,
              'recommend_uid':self.recommend_uid}
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
Index('recommend_media_main_index',RecommendMedia.uid,RecommendMedia.recommend_uid)