from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker,Session
import redis
import memcache
import qiniu.conf
class AutoSession(Session):
    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
db=create_engine("mysql://root:123456@192.173.1.213:4040/site?charset=utf8",pool_recycle=60,echo=True)
DBBase=declarative_base(name="DBBase")
#Session = sessionmaker(bind=db)
Session = sessionmaker(bind=db,autocommit=False,autoflush=False,class_=AutoSession)

redisdb=redis.StrictRedis(host='192.173.1.213', port=6379)
memclient=memcache.Client(['192.173.1.213:11211'])

qiniu.conf.ACCESS_KEY = "x5yGWWp6fBGMwlJyEU0GVzilkNIa7Mc87ibrKpdU"
qiniu.conf.SECRET_KEY = "r_8i1p4LCaiI0isFxuF2paAKhoQotGeqngCD4B1O"
qiniuSpace="kidswant"