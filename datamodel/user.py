__author__ = 'amen'
from sqlalchemy import *
import dbconfig
class User(dbconfig.DBBase):
    __tablename__ = 'user'
    uid=Column(BigInteger,autoincrement=True,primary_key=True,nullable=False)
    phone=Column(String(40),unique=True,nullable=False)
    nick=Column(String(256))
    password=Column(String(128))
    headpic=Column(String(1024))
    sex=Column(Integer,default=0)
    birthday = Column(DateTime)
    marriage = Column(Integer)
    background_image = Column(String(1024))
    height = Column(Integer, default=0)
    create_time=Column(TIMESTAMP,server_default=text('CURRENT_TIMESTAMP'))

    def toJson(self):
        return {"uid":self.uid,
                "nick":self.nick,
                "headpic":self.headpic,
                "sex":self.sex,
                "birthday":self.birthday,
                "marriage":self.marriage,
                "background_image":self.background_image,
                "height":self.height,
                "create_time":self.create_time}