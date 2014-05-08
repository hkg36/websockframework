#coding:utf-8
import msgpack
import datetime
import time
def encode_datetime(obj):
    if isinstance(obj, datetime.datetime):
        return time.mktime(obj.timetuple())
    return obj
packer=msgpack.Packer(default=encode_datetime,use_single_float=True)
packed=packer.pack({"aa":u"大家好","bb":datetime.datetime.now()})
print packed
res=msgpack.unpackb(packed,encoding="utf-8")
print res