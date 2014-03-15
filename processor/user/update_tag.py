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
    exdata=UserExData.objects(uid=BackEndEnvData.uid).first()
    if exdata is None:
        exdata=UserExData(uid=BackEndEnvData.uid)
    exdata.tags=tags
    exdata.save()
    return Res()