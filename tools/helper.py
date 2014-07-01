__author__ = 'amen'
try:
    import GeoCombine
except Exception,e:
    GeoCombine=None
import time
import datetime
import json
import dbconfig
import cPickle as pickle
import urllib
from Crypto.Cipher import AES
import msgpack
import base64
import random
import uuid
import leveldb

def Res(res={},errno=0,error='no error'):
    return {"errno":errno,"error":error,"result":res}
def GetFileLink(db_file_record):
    return db_file_record

def LoadEvent(event):
    event_type=event['type']
    if event_type=='add_friend':
        data= {'eid':event['eid'],
                'create_time':event['create_time'],
                'type':event_type,
                'uid':event['param1'],}
        if event.get('param2'):
            data['add_type']=event.get('param2')
        return data
    elif event_type=='group_invite':
        return  {'eid':event['eid'],
                'create_time':event['create_time'],
                'type':event_type,
                'gid':event['param1'],
                'fromuid':event['param2']}
    elif event_type=='recommend':
        return  {'eid':event['eid'],
                'create_time':event['create_time'],
                'type':event_type,
                'uid':event['param1'],
                'recommend_uid':event['param2']
        }
    elif event_type=='request_join_circle':
        return {'eid':event['eid'],
                'create_time':event['create_time'],
                'type':event_type,
                'uid':event['param1'],
                'cid':event['param2']}
    elif event_type=="accept_join_circle":
        return {'eid':event['eid'],
                'create_time':event['create_time'],
                'type':event_type,
                'cid':event['param1'],
                'roleid':event['param2'],
                'by_uid':event['param3']
                }

def CombineGeo(long,lat):
    lat_int=int((lat+90)*10e6)
    long_int=int((long+180)*10e6)
    if GeoCombine:
        return GeoCombine.Combine(long_int,lat_int)
    else:
        result=0;
        for i in xrange(32): #sizeof(unsigned int)*8;i++)
            mid=long_int&(0x1<<i);
            result|=mid<<i;

        for i in xrange(32):
            mid=lat_int&(0x1<<i);
            result|=mid<<(i+1);
        return result;

class AutoFitJson(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj,datetime.datetime):
            return time.mktime(obj.timetuple())
        return json.JSONEncoder.default(self, obj)
DefJsonEncoder=AutoFitJson(skipkeys=False,
    check_circular=True,
    allow_nan=True,
    indent=None,
    encoding='utf-8',
    default=None,ensure_ascii=False,separators=(',', ':'))

def script_path():
    import inspect, os
    caller_file = inspect.stack()[1][1]         # caller's filename
    return os.path.abspath(os.path.dirname(caller_file))# path

def FunctionCache(timeout=20):
    def ACF(fun):
        def Work(*args,**kwargs):
            fkey= 'funcCache:%s.%s(%s%s)'%(fun.__module__,fun.__name__,DefJsonEncoder.encode(args) if args else '',DefJsonEncoder.encode(kwargs) if kwargs else '')
            fkey=urllib.quote(fkey)
            print fkey
            result=dbconfig.memclient.get(fkey)
            if result is None:
                res=fun(*args,**kwargs)
                result=pickle.dumps(res,pickle.HIGHEST_PROTOCOL)
                dbconfig.memclient.set(fkey,result,timeout,128)
                return res
            else:
                return pickle.loads(result)
        return Work
    return ACF
bufferleveldb=None
def LocalBuffer(timeout=30):
    def ACF(fun):
        def Work(*args,**kwargs):
            global bufferleveldb
            if not bufferleveldb:
                filename='/tmp/%d.leveldb'%random.randint(100000000000,1000000000000)
                bufferleveldb=leveldb.LevelDB(filename)
            keyname='%s.%s(%s,%s)'%(fun.__module__,fun.__name__,json.dumps(args),json.dumps(kwargs))
            #print keyname
            try:
                buffered=bufferleveldb.Get(keyname)
                buffres=msgpack.unpackb(buffered)
                if time.time()- buffres['time']<timeout:
                    #print 'use buffer'
                    return pickle.loads(buffres['res'])
            except Exception,e:
                pass
            funres=fun(*args,**kwargs)
            bufferleveldb.Put(keyname,msgpack.packb({'res':pickle.dumps(funres),'time':time.time()}))
            return funres
        return Work
    return ACF

session_crypt_key=b'7Y9VZl9M3HDmDfnb'
session_crypt_head='x\xaa\x83\xd4\xf3d\x01\xfa\xaf\x84\xfe;\xde\xd2o\x08'
def BuildCryptSession(uid):
    data=msgpack.packb([uuid.uuid4().get_bytes(),time.time(),uid])
    cipher = AES.new(session_crypt_key, AES.MODE_CFB, session_crypt_head)
    msg = cipher.encrypt(data)
    msg64=base64.b16encode(msg)
    return "SCK_"+msg64
def DecodeCryptSession(sessionid):
    if sessionid.startswith('SCK_')==False:
        return None
    try:
        msg64=sessionid[4:]
        msg=base64.b16decode(msg64)
        cipher = AES.new(session_crypt_key, AES.MODE_CFB, session_crypt_head)
        data=cipher.decrypt(msg)
        srcdata=msgpack.unpackb(data)
    except Exception,e:
        return None
    return {'uid':srcdata[2],'time':srcdata[1],'uuid':srcdata[0]}
if __name__ == '__main__':
    session= BuildCryptSession(223)
    print(session)
    print DecodeCryptSession(session)