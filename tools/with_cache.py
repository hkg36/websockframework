#coding:utf8
from sqlalchemy import and_
from datamodel.Endorsement import Endorsement, EndorsementInfo
from datamodel.merchandise import StoreMerchandise
from datamodel.user import UserExData, User
from datamodel.user_circle import UserCircle, CircleRole, CircleDef

import helper
import dbconfig
@helper.FunctionCache()
def GetUserInfo(uid):
    session=dbconfig.ReadSession()
    with helper.AutoClose(session) as autoclose:
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

        user_endorsinfo=session.query(EndorsementInfo).filter(EndorsementInfo.uid==uid).first()

        user_endors=[]
        for epair in session.query(Endorsement).filter(Endorsement.uid==uid).all():
            user_endors.append({'slogan':epair.slogan,'create_time':epair.create_time,'merchandise':GetMerchandise(epair.mid)})

        resultobj={"user":user.toJson()}
        if userexdata is not None:
            resultobj['exdata']=userexdata.toJson()
        if circles:
            resultobj['circles']=circles
        if user_endorsinfo:
            resultobj['endorsement']=user_endorsinfo.toJson()
        if user_endors:
            resultobj['endors_list']=user_endors
    return resultobj


@helper.FunctionCache()
def GetMerchandise(mid):
    with dbconfig.Session() as session:
        sm=session.query(StoreMerchandise).filter(StoreMerchandise.mid==mid).first()
        if not sm:
            return None
        return sm.toJson2()