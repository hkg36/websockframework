__author__ = 'amen'
from sqlalchemy import *
import dbconfig
import time
class Events(dbconfig.DBBase):
    __tablename__ = 'events'
    eid=Column(BigInteger,autoincrement=True,primary_key=True,nullable=False)
    touid=Column(BigInteger,nullable=False)
    type=Column(String(32),nullable=False)
    param1=Column(BigInteger)
    param2=Column(BigInteger)
    param3=Column(BigInteger)
    create_time=Column(TIMESTAMP,server_default=text('CURRENT_TIMESTAMP'))
    __table_args__=({'mysql_engine':'MyISAM'},)

    def toJson(self):
        return {'eid':self.eid,
                'touid':self.touid,
                'type':self.type,
                'param1':self.param1,
                'param2':self.param2,
                'param3':self.param3,
                'create_time':time.mktime(self.create_time.timetuple())}