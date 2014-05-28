#coding:utf-8
from datamodel.user import UserInviteLog, User
from tools.helper import Res, DefJsonEncoder
from tools.session import CheckSession
import BackEndEnvData
import dbconfig
import datetime

SEND_SMS=True
@CheckSession()
def run():
    alllog=UserInviteLog.objects(uid=BackEndEnvData.uid)
    loglist=[]
    for one in alllog:
        loglist.append(one.toJson())
    return Res({'invites':loglist})
