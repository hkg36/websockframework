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
    time=Column(TIMESTAMP,server_default=text('CURRENT_TIMESTAMP'))
    def toJson(self):
        data={'msgid':self.msgid,
              'fromid':self.fromid,
              'toid':self.toid,
              'content':self.content,
              'time':time.mktime(self.time.timetuple())}
        if self.picture:
            data['picture']=self.picture
            data['width']=self.width
            data['height']=self.height
        if self.video:
            data['video']=self.video
            data['length']=self.length
        if self.voice:
            data['voice']=self.voice
            data['length']=self.length
        return data