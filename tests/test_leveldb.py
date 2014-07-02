__author__ = 'amen'
import leveldb
import datetime
from bson import BSON
db=leveldb.LevelDB("/tmp/test.leveldb")
db.Put("aaa0",BSON.encode({"user": 0}))
db.Put("sss1",BSON.encode({"uid": datetime.datetime.now()}))
db.Put("sss2",BSON.encode({"user": 2}))
db.Put("ddd2",BSON.encode({"user": 3}))
iter=db.RangeIter('sss',fill_cache=False)

for k,v in iter:
    print k,BSON(v).decode()