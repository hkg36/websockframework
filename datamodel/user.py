__author__ = 'amen'
from sqlalchemy import *
import dbconfig
import time
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
    actor_level=Column(Integer,default=0)
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
                "create_time":time.mktime(self.create_time.timetuple())}
        if self.active_time:
            data["active_time"]=time.mktime(self.active_time.timetuple())
        if showphone:
            data['phone']=self.phone
        return data