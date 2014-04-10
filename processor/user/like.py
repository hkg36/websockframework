from datamodel.user import UserExData
from tools.helper import Res
from tools.session import CheckSession

__author__ = 'amen'
import BackEndEnvData
import dbconfig


@CheckSession()
def run(uid):
    if uid==BackEndEnvData.uid:
        return Res(errno=2,error="like self")
    UserExData.objects(uid=uid).update_one(inc__like_me_count=1)
    return Res()