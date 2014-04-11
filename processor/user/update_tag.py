from datamodel.user import User, UserExData
from tools.helper import Res
from tools.session import CheckSession

__author__ = 'amen'
import BackEndEnvData
import dbconfig


@CheckSession()
def run(tags):
    if isinstance(tags,list)==False:
        return Res(errno=2,error="value type error")
    tags=list(set(tags))
    UserExData.objects(uid=BackEndEnvData.uid).update_one(upsert=True,set__tags=tags)
    return Res()