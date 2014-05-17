#coding:utf-8
__author__ = 'amen'
from sqlalchemy import *
import dbconfig

class CircleDef(dbconfig.DBBase):
    __tablename__ = 'circle_define'
    cid=Column(Integer,nullable=False,autoincrement=True,primary_key=True)
    name=Column(String(32))
    board=Column(String(256))
    store_group_id=Column(Integer,default=0)
    poster_url=Column(String(1024))
    interact_poster=Column(SmallInteger,default=0)

    def toJson(self):
        return {"cid":self.cid,
                "name":self.name,
                "board":self.board,
                "store_group_id":self.store_group_id,
                "poster_url":self.poster_url,
                "interact_poster":self.interact_poster}

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
    cid=Column(Integer,nullable=False)
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