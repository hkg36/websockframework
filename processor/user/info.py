#coding:utf-8
from sqlalchemy import and_
from datamodel.user import User,UserExData
from datamodel.user_circle import UserCircle, CircleDef
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
        users_circle=session.query(UserCircle,CircleDef)\
            .join(CircleDef,and_(CircleDef.cid==UserCircle.cid,CircleDef.subid==UserCircle.subid))\
            .filter(UserCircle.uid.in_(uid)).all()
        circles={}
        for uc,cdef in users_circle:
            ll=circles.get(uc.uid,[])
            ll.append({'cid':uc.cid,'subid':uc.subid,'title':cdef.title,'level':cdef.level,'time':uc.time})
            circles[uc.uid]=ll

        users=session.query(User).filter(User.uid.in_(uid)).all()
        ulist=[]
        for user in users:
            uinfo=user.toJson()
            uinfo['exinfo']=userexinfo.get(user.uid,None)
            uinfo['circle']=circles.get(user.uid,None)
            ulist.append(uinfo)
    return Res({"users":ulist})