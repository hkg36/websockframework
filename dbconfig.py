from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker,Session
import redis
import memcache
import qiniu.conf
import mongoengine
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
mongoengine.connect('Site',host='mongodb://192.173.1.213:27010/')

qiniu.conf.ACCESS_KEY = "W4nYpf8HOCEyCzjLHpO0QVYGOykRucI1MIniLpgL"
qiniu.conf.SECRET_KEY = "3NRgrf8v_XHGGoWROaXYZoFYPvSeN3HnI_19eVfk"
qiniuSpace="laixinle"
qiniuDownLoadLinkHead="http://%s.qiniudn.com/"%qiniuSpace