#encoding:utf8
__author__ = 'amen'
import leveldb
import datetime
import uuid
from bson import BSON
db=leveldb.LevelDB("/tmp/test.leveldb")
db.Put("aaa0",BSON.encode({"user": 0}))
db.Put("sss1",BSON.encode({"uid": datetime.datetime.now()}))
db.Put("sss2",BSON.encode({"user": uuid.uuid4()}))
db.Put("sss3",BSON.encode({"user": "主席好"}))
db.Put("ddd2",BSON.encode({"user": u"大家好"}))
iter=db.RangeIter('sss',fill_cache=False)

for k,v in iter:
    print k,BSON(v).decode()