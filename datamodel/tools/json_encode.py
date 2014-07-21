import json
import datetime
import time

from sqlalchemy.ext.declarative import DeclarativeMeta


def new_alchemy_encoder():
    _visited_objs = []
    class AlchemyEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj.__class__, DeclarativeMeta):
                # don't re-visit self
                if obj in _visited_objs:
                    return None
                _visited_objs.append(obj)

                # an SQLAlchemy class
                fields = {}
                for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
                    chkattr=getattr(obj,field)
                    if hasattr(chkattr, '__call__') == False:
                        fields[field] = chkattr
                # a json-encodable dict
                return fields
            elif isinstance(obj,datetime.datetime):
                return time.mktime(obj.timetuple())
            return json.JSONEncoder.default(self, obj)
    return AlchemyEncoder
