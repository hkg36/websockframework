from sqlalchemy import *
import dbconfig
class ConnectionInfo(dbconfig.DBBase):
    __tablename__ = 'connection_info'
    uid = Column(BigInteger, primary_key=True,nullable=False)
    queue_id =  Column(String(128),index=True,nullable=False)
    connection_id = Column(String(128),nullable=False)

    __table_args__ = (UniqueConstraint('connection_id', 'queue_id'),)
