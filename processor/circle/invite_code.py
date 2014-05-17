from sqlalchemy import and_
from tools.session import CheckSession, GenSession

__author__ = 'amen'
from datamodel.user_circle import CircleDef,CircleRole, UserCircle
from tools.helper import Res, DefJsonEncoder
import BackEndEnvData
import dbconfig

@CheckSession()
def run(cid,roleid):
    with dbconfig.Session() as session:
        self_uc=session.query(UserCircle).filter(and_(UserCircle.uid==BackEndEnvData.uid,UserCircle.cid==cid)).first()
        if self_uc is None:
            return Res(errno=2,error="not in circle")
        if roleid!=self_uc.roleid:
            circles=session.query(CircleRole).filter(and_(CircleRole.cid==cid,CircleRole.roleid.in_((roleid,self_uc.roleid)))).all()
            self_level=0
            to_set_level=10000000
            for ci in circles:
                if ci.roleid==roleid:
                    to_set_level=ci.level
                elif ci.roleid==self_uc.roleid:
                    self_level=ci.level
            if self_level<to_set_level:
                return Res(errno=2,error="level too low")

        vcode=GenSession(8)
        dbconfig.memclient.set("circleinvite:"+vcode,DefJsonEncoder.encode({"uid":BackEndEnvData.uid,"cid":cid,"roleid":roleid}),time=45*60)
        return Res({"vcode":vcode})