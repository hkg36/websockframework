#coding:utf-8
from sqlalchemy import and_
from datamodel.user import User,UserExData
from datamodel.user_circle import UserCircle, CircleDef, CircleRole
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
        users_circle=session.query(UserCircle,CircleRole,CircleDef)\
            .join(CircleRole,and_(CircleRole.cid==UserCircle.cid,CircleRole.roleid==UserCircle.roleid))\
            .join(CircleDef,CircleDef.cid==UserCircle.cid)\
            .filter(UserCircle.uid.in_(uid)).all()
        circles={}
        for uc,cr,cd in users_circle:
            ll=circles.get(uc.uid,[])
            linedata=uc.toJson()
            del linedata['uid']
            linedata.update(cr.toJson())
            linedata.update(cd.toJson())
            ll.append(linedata)
            circles[uc.uid]=ll

        users=session.query(User).filter(User.uid.in_(uid)).all()
        ulist=[]
        for user in users:
            uinfo=user.toJson()
            uinfo['exinfo']=userexinfo.get(user.uid,None)
            uinfo['circle']=circles.get(user.uid,None)
            ulist.append(uinfo)
    return Res({"users":ulist})