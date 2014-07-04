__author__ = 'amen'
import json
import datetime
import time
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