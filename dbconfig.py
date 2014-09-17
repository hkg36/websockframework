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
db=create_engine("mysql://root:123456@mysql1.master.lfs.server:3306/site?charset=utf8",pool_recycle=60,echo=True)
#readdb=create_engine("mysql://root:123456@192.173.1.212:3306/site?charset=utf8",pool_recycle=60,echo=True)
DBBase=declarative_base(name="DBBase")
#Session = sessionmaker(bind=db)
Session = sessionmaker(bind=db,autocommit=False,autoflush=False,class_=AutoSession)
ReadSession=Session#sessionmaker(bind=readdb,autocommit=False,autoflush=False,class_=AutoSession)

redisdb=redis.StrictRedis(host='redis1.lfs.server', port=6379)
memclient=memcache.Client(['memcache1.lfs.server:11211'])
mongoengine.connect('Site',host='mongodb://mongodb.rs0.master.lfs.server:27010/')

qiniu.conf.ACCESS_KEY = "W4nYpf8HOCEyCzjLHpO0QVYGOykRucI1MIniLpgL"
qiniu.conf.SECRET_KEY = "3NRgrf8v_XHGGoWROaXYZoFYPvSeN3HnI_19eVfk"
qiniuSpace="laixinle"
qiniuDownLoadLinkHead="http://%s.qiniudn.com/"%qiniuSpace