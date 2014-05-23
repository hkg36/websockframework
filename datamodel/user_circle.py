#coding:utf-8
__author__ = 'amen'
from sqlalchemy import *
from mongoengine import *
import dbconfig
import datetime

class CircleDef(dbconfig.DBBase):
    __tablename__ = 'circle_define'
    cid=Column(Integer,nullable=False,autoincrement=True,primary_key=True)
    name=Column(String(32))
    board=Column(String(256))
    store_group_id=Column(Integer,default=0)
    poster_url=Column(String(1024))
    interact_poster=Column(SmallInteger,default=0)
    icon_url=Column(String(1024))

    def toJson(self):
        return {"cid":self.cid,
                "name":self.name,
                "board":self.board,
                "store_group_id":self.store_group_id,
                "poster_url":self.poster_url,
                "interact_poster":self.interact_poster,
                "icon_url":self.icon_url}
class CircleExList(dbconfig.DBBase): #外部插件列表
    __tablename__ = 'circle_ex_list'
    ceid=Column(Integer,nullable=False,autoincrement=True,primary_key=True)
    cid=Column(Integer,nullable=False,index=True)
    title=Column(String(16))
    url=Column(String(1024))
    time=Column(TIMESTAMP,server_default=text('CURRENT_TIMESTAMP'))
    def toJson(self):
        return {'title':self.title,
                'url':self.url,
                'time':self.time}

class CircleBoardHistory(dbconfig.DBBase):
    __tablename__ = 'circle_board_history'
    bid=Column(Integer,nullable=False,autoincrement=True,primary_key=True)
    cid=Column(Integer,index=True,nullable=False)
    board=Column(String(256),nullable=False)
    time=Column(TIMESTAMP,server_default=text('CURRENT_TIMESTAMP'))
    def toJson(self):
        return {"bid":self.bid,
                "cid":self.cid,
                "board":self.board,
                "time":self.time}

class CircleRole(dbconfig.DBBase):
    __tablename__ = 'circle_role'
    cid=Column(Integer,nullable=False)
    roleid=Column(Integer,nullable=False,default=0)
    level=Column(Integer,nullable=False,default=0)
    title=Column(String(32),nullable=False)
    __table_args__ = (PrimaryKeyConstraint('cid', 'roleid'),)

    def toJson(self):
        return {"cid":self.cid,
                "roleid":self.roleid,
                "level":self.level,
                "title":self.title}

class UserCircle(dbconfig.DBBase):
    __tablename__ = 'circle_user'
    uid=Column(BigInteger,nullable=False)
    cid=Column(Integer,nullable=False,index=True)
    roleid=Column(Integer,nullable=False,default=0)
    time=Column(TIMESTAMP,server_default=text('CURRENT_TIMESTAMP'))
    by_uid=Column(BigInteger)

    __table_args__ = (PrimaryKeyConstraint('uid','cid'),)
    def toJson(self):
        return {"uid":self.uid,
                "cid":self.cid,
                "roleid":self.roleid,
                'time':self.time,
                "by_uid":self.by_uid}

class LikeRecord(EmbeddedDocument):
    uid=LongField(required=True)
    time=DateTimeField(default=datetime.datetime.now)
    def toJson(self):
        return {'uid':self.uid,
                "time":self.time}
class ReplyRecord(EmbeddedDocument):
    uid=LongField(required=True)
    content=StringField(required=True)
    time=DateTimeField(default=datetime.datetime.now)
    def toJson(self):
        return {"uid":self.uid,
                "content":self.content,
                'time':self.time}
class CirclePost(Document):
    postid=SequenceField(primary_key=True)
    uid=LongField(required=True)
    cid=IntField(required=True)
    content=StringField()
    picture_list=ListField(URLField())
    likes=ListField(EmbeddedDocumentField(LikeRecord))
    replys=ListField(EmbeddedDocumentField(ReplyRecord))
    time=DateTimeField(default=datetime.datetime.now)
    def toJson(self):
        data= {'postid':self.postid,
                'uid':self.uid,
                'cid':self.cid,
                'picture_list':[one for one in self.picture_list],
                'likes':[one.toJson() for one in self.likes],
                'replys':[one.toJson() for one in self.replys],
                'content':self.content,
                'time':self.time,
                }
        return data

    meta = {
        'indexes': [('cid','-postid'),]
    }