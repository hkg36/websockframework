#coding:utf-8
__author__ = 'amen'
from sqlalchemy import *
import dbconfig
import time
class Message(dbconfig.DBBase):
    __tablename__ = 'message'
    msgid=Column(BigInteger,autoincrement=True,primary_key=True,nullable=False)
    fromid=Column(BigInteger,nullable=False,index=True)
    toid=Column(BigInteger,nullable=False,index=True)
    content=Column(String(4096))
    picture=Column(String(1024))
    video=Column(String(1024))
    voice=Column(String(1024))
    width=Column(Integer)
    height=Column(Integer)
    length=Column(Integer)
    lat=Column(Float)
    long=Column(Float)
    time=Column(TIMESTAMP,server_default=text('CURRENT_TIMESTAMP'))
    def toJson(self):
        data={'msgid':self.msgid,
              'fromid':self.fromid,
              'toid':self.toid,
              'time':self.time}
        if self.content:
            data['type']='txt'
            data['content']=self.content
        elif self.picture:
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
        elif self.lat and self.long:
            data['type']="geo"
            data['lat']=self.lat
            data['long']=self.long
        return data