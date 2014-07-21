__author__ = 'amen'
import json
import ujson
import datetime
import time
class AutoFitJson(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj,datetime.datetime):
            return time.mktime(obj.timetuple())
        return json.JSONEncoder.default(self, obj)
class JSONProxy:
    @staticmethod
    def encode(obj):
        return ujson.dumps(obj,ensure_ascii=False)
    @staticmethod
    def decode(data):
        return ujson.loads(data)
#DefJsonEncoder=JSONProxy
DefJsonEncoder=AutoFitJson(skipkeys=False,
    check_circular=True,
    allow_nan=True,
    indent=None,
    encoding='utf-8',
    default=None,ensure_ascii=False,separators=(',', ':'))