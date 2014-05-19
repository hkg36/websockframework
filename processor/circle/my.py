#coding:utf-8
from sqlalchemy import and_
from datamodel.user import User,UserExData
from datamodel.user_circle import UserCircle, CircleDef, CircleRole
from tools.helper import Res
from tools.session import CheckSession
import dbconfig
import BackEndEnvData

@CheckSession()
def run():
    with dbconfig.Session() as session:
        users_circle=session.query(UserCircle,CircleRole,CircleDef)\
            .join(CircleRole,and_(CircleRole.cid==UserCircle.cid,CircleRole.roleid==UserCircle.roleid))\
            .join(CircleDef,CircleDef.cid==UserCircle.cid)\
            .filter(UserCircle.uid==BackEndEnvData.uid).all()
        circles=[]
        for uc,cr,cd in users_circle:
            linedata=uc.toJson()
            del linedata['uid']
            linedata.update(cr.toJson())
            linedata.update(cd.toJson())
            circles.append(linedata)

    return Res({"circles":circles})