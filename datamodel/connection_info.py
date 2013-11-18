from sqlalchemy import *
import dbconfig
class ConnectionInfo(dbconfig.DBBase):
    __tablename__ = 'connection_info'
    client_id = Column(Integer, primary_key=True,nullable=False)
    queue_id =  Column(String(128),index=True,nullable=False)
    connection_id = Column(String(128),unique=True,nullable=False)
