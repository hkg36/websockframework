from datamodel.user import UserExData
from tools.helper import Res
from tools.session import CheckSession

__author__ = 'amen'
import BackEndEnvData
import dbconfig


@CheckSession()
def run(uids):
    if isinstance(uids,list)==False:
        uids=[uids]
    ulist=[]
    for exdata in UserExData.objects(uid__in=uids):
        ulist.append({"uid":exdata.uid,"tags":exdata.tags})
    return Res({"tags":ulist})