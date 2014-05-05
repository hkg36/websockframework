from sqlalchemy import and_
from tools.session import CheckSession, GenSession

__author__ = 'amen'
from datamodel.user_circle import CircleDef, UserCircle
from tools.helper import Res, DefJsonEncoder
import BackEndEnvData
import dbconfig

@CheckSession()
def run(cid,subid):
    with dbconfig.Session() as session:
        self_uc=session.query(UserCircle).filter(and_(UserCircle.uid==BackEndEnvData.uid,UserCircle.cid==cid)).first()
        if self_uc is None:
            return Res(errno=2,error="not in circle")
        if subid!=self_uc.subid:
            circles=session.query(CircleDef).filter(and_(CircleDef.cid==cid,CircleDef.subid.in_((subid,self_uc.subid)))).all()
            self_level=0
            to_set_level=10000000
            for ci in circles:
                if ci.subid==subid:
                    to_set_level=ci.level
                elif ci.subid==self_uc.subid:
                    self_level=ci.level
            if self_level<to_set_level:
                return Res(errno=2,error="level too low")

        vcode=GenSession(8)
        dbconfig.memclient.set("circleinvite:"+vcode,DefJsonEncoder.encode({"uid":BackEndEnvData.uid,"cid":cid,"subid":subid}),time=45*60)
        return Res({"vcode":vcode})