__author__ = 'amen'
from sqlalchemy import *
import dbconfig
class Group(dbconfig.DBBase):
    __tablename__ = 'group'
    gid=Column(BigInteger,autoincrement=True,primary_key=True,nullable=False)
    creator=Column(BigInteger,nullable=False,index=True)
    group_name=Column(String(256),nullable=False)
    group_board=Column(String(4096))
    type=Column(Integer)
    time=Column(TIMESTAMP,server_default=text('CURRENT_TIMESTAMP'))

    def toJson(self):
        return {'gid':self.gid,
                "creator":self.creator,
                "name":self.group_name,
                "board":self.group_board,
                "type":self.type,
                "time":self.time}