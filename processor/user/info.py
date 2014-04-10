#coding:utf-8
from datamodel.user import User,UserExData
from tools.helper import Res
from tools.session import CheckSession
import dbconfig


@CheckSession()
def run(uid):
    if isinstance(uid,list)==False:
        uid=[uid]
    with dbconfig.Session() as session:
        userexdatalist=UserExData.objects(uid__in=uid)
        userexinfo={}
        for exinfo in userexdatalist:
            userexinfo[exinfo.uid]=exinfo.toJson()
        users=session.query(User).filter(User.uid.in_(uid)).all()
        ulist=[]
        for user in users:
            uinfo=user.toJson()
            uinfo['exinfo']=userexinfo.get(user.uid,None)
            ulist.append(uinfo)
    return Res({"users":ulist})