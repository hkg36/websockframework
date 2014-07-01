__author__ = 'amen'
import json
def FunctionShell(timeout=30):
    def ACF(fun):
        def Work(*args,**kwargs):
            print dir(fun)
            print '%s.%s(%s,%s)'%(fun.__module__,fun.__name__,json.dumps(args),json.dumps(kwargs))
            return fun(*args,**kwargs)
        return Work
    return ACF

import leveldb
import pickle
import msgpack
import time
import random
bufferleveldb=None
def LocalBuffer(timeout=30):
    def ACF(fun):
        def Work(*args,**kwargs):
            global bufferleveldb
            if not bufferleveldb:
                filename='/tmp/%d.leveldb'%random.randint(100000000000,1000000000000)
                bufferleveldb=leveldb.LevelDB(filename)
            keyname='%s.%s(%s,%s)'%(fun.__module__,fun.__name__,json.dumps(args),json.dumps(kwargs))
            print keyname
            try:
                buffered=bufferleveldb.Get(keyname)
                buffres=msgpack.unpackb(buffered)
                if time.time()- buffres['time']<timeout:
                    print 'use buffer'
                    return pickle.loads(buffres['res'])
            except Exception,e:
                pass
            funres=fun(*args,**kwargs)
            bufferleveldb.Put(keyname,msgpack.packb({'res':pickle.dumps(funres),'time':time.time()}))
            return funres
        return Work
    return ACF
@LocalBuffer()
def PP(aa,bb=2):
    return aa*bb