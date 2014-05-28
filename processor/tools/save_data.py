#coding:utf-8
from datamodel.user import User, UserExData
from tools.helper import Res
from tools.session import CheckSession
import BackEndEnvData

@CheckSession()
def run(**kwargs):
    if not kwargs:
        return Res(errno=3,error="not value")
    uexd=UserExData.objects(uid=BackEndEnvData.uid).first()
    if uexd is None:
        uexd=UserExData()
        uexd.uid=BackEndEnvData.uid
    uexd.client_data.update(kwargs)
    uexd.save()
    return Res()