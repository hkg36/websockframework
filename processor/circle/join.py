from sqlalchemy import and_
from tools.session import CheckSession, GenSession

__author__ = 'amen'
from datamodel.user_circle import CircleDef,CircleRole, UserCircle
from tools.helper import Res, DefJsonEncoder
import BackEndEnvData
import dbconfig
import json

@CheckSession()
def run(vcode):
    codedata=dbconfig.memclient.get(("circleinvite:"+vcode).encode("utf-8"))
    if codedata is None:
        return Res(errno=3,error="not vcode")
    data=json.loads(codedata)
    if data['uid']==BackEndEnvData.uid:
        return Res(errno=2,error="not self invite")
    with dbconfig.Session() as session:
        self_uc=session.query(UserCircle).filter(and_(UserCircle.uid==BackEndEnvData.uid,UserCircle.cid==data['cid'])).first()
        if self_uc:
            if self_uc.roleid==data['roleid']:
                return Res({"circle":{"cid":self_uc.cid,"roleid":self_uc.roleid}})
            to_set_cd=session.query(CircleRole).filter(and_(CircleRole.cid==data['cid'],CircleRole.roleid==data['roleid'])).first()
            self_cd=session.query(CircleRole).filter(and_(CircleRole.cid==self_uc.cid,CircleRole.roleid==self_uc.roleid)).first()
            if self_cd.level>to_set_cd.level:
                return Res(errno=2,error="can not lower level")
        self_uc=UserCircle()
        self_uc.uid=BackEndEnvData.uid
        self_uc.cid=data['cid']
        self_uc.roleid=data['roleid']
        self_uc.by_uid=data['uid']
        self_uc=session.merge(self_uc)
        session.commit()
        return Res({"circle":{"cid":self_uc.cid,"roleid":self_uc.roleid}})
