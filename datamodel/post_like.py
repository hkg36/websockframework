__author__ = 'amen'
from sqlalchemy import *
import dbconfig
class PostLike(dbconfig.DBBase):
    __tablename__ = 'post_like'
    postid=Column(BigInteger,nullable=False)
    uid=Column(BigInteger,nullable=False)
    time=Column(TIMESTAMP,server_default=text('CURRENT_TIMESTAMP'))