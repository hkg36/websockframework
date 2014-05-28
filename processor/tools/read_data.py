#coding:utf-8
import random
from datamodel.user import User, UserExData
from tools.helper import Res
from tools.session import CheckSession
import dbconfig
import BackEndEnvData
import tools.addPushQueue

@CheckSession()
def run():
    uexd=UserExData.objects(uid=BackEndEnvData.uid).first()
    if uexd is None:
        return Res()
    else:
        return Res(uexd.client_data)