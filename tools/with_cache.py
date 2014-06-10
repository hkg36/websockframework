#coding:utf8
from sqlalchemy import and_
from datamodel.user import UserExData, User
from datamodel.user_circle import UserCircle, CircleRole, CircleDef

import helper
import dbconfig
@helper.FunctionCache()
def GetUserInfo(uid):
    with dbconfig.Session() as session:
        userexdata=UserExData.objects(uid=uid).first()
        users_circle=session.query(UserCircle,CircleRole,CircleDef)\
            .join(CircleRole,and_(CircleRole.cid==UserCircle.cid,CircleRole.roleid==UserCircle.roleid))\
            .join(CircleDef,CircleDef.cid==UserCircle.cid)\
            .filter(UserCircle.uid==uid).all()
        circles=[]
        for uc,cr,cd in users_circle:
            linedata=uc.toJson()
            del linedata['uid']
            linedata.update(cr.toJson())
            linedata.update(cd.toJson())
            circles.append(linedata)

        user=session.query(User).filter(User.uid==uid).first()

        resultobj={"user":user.toJson()}
        if userexdata is not None:
            resultobj['exdata']=userexdata.toJson()
        if circles:
            resultobj['circles']=circles
    return resultobj
