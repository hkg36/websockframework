__author__ = 'amen'
import leveldb

db=leveldb.LevelDB("/tmp/test.leveldb")
db.Put("aaa0",'00000')
db.Put("sss1","11111")
db.Put("sss2","22222")
db.Put("ddd2","22222")
iter=db.RangeIter('sss',fill_cache=False)

for k in iter:
    print k