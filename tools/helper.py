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

def Res(res={},errno=0,error='no error'):
    return {"errno":errno,"error":error,"result":res}
def GetFileLink(db_file_record):
    return db_file_record

def LoadEvent(event):
    event_type=event['type']
    if event_type=='add_friend':
        return {'eid':event['eid'],
                'create_time':event['create_time'],
                'type':event_type,
                'uid':event['param1']}
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
if __name__ == '__main__':
    print CombineGeo(147.9873,32.5678)