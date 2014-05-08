from sqlalchemy import and_
from tools.session import CheckSession, GenSession

__author__ = 'amen'
from datamodel.user_circle import CircleDef, UserCircle
from tools.helper import Res, DefJsonEncoder
import BackEndEnvData
import dbconfig
import json

@CheckSession()
def run(uid,cid=None):
    if uid==BackEndEnvData.uid:
        return Res(errno=2,error="not self invite")
    with dbconfig.Session() as session:
        findparam=UserCircle.uid==uid
        if cid != None:
            findparam=and_(findparam,UserCircle.cid==cid)
        by_user_c=session.query(UserCircle).filter(findparam).order_by(UserCircle.time).first()
        if by_user_c is None:
            return Res(errno=3,error="user not in any circle")
        self_uc=session.query(UserCircle).filter(and_(UserCircle.uid==BackEndEnvData.uid,UserCircle.cid==by_user_c.cid)).first()
        if self_uc:
            if self_uc.subid==by_user_c.subid:
                return Res({"circle":{"cid":self_uc.cid,"subid":self_uc.subid}})
            to_set_cd=session.query(CircleDef).filter(and_(CircleDef.cid==by_user_c.cid,CircleDef.subid==by_user_c.subid)).first()
            self_cd=session.query(CircleDef).filter(and_(CircleDef.cid==self_uc.cid,CircleDef.subid==self_uc.subid)).first()
            if self_cd.level>to_set_cd.level:
                return Res(errno=2,error="can not lower level")
        self_uc=UserCircle()
        self_uc.uid=BackEndEnvData.uid
        self_uc.cid=by_user_c.cid
        self_uc.subid=by_user_c.subid
        self_uc.by_uid=by_user_c.uid
        self_uc=session.merge(self_uc)
        session.commit()
        return Res({"circle":{"cid":self_uc.cid,"subid":self_uc.subid}})