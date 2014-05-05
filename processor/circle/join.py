from sqlalchemy import and_
from tools.session import CheckSession, GenSession

__author__ = 'amen'
from datamodel.user_circle import CircleDef, UserCircle
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
            if self_uc.subid==data['subid']:
                return Res({"circle":{"cid":self_uc.cid,"subid":self_uc.subid}})
            to_set_cd=session.query(CircleDef).filter(and_(CircleDef.cid==data['cid'],CircleDef.subid==data['subid'])).first()
            self_cd=session.query(CircleDef).filter(and_(CircleDef.cid==self_uc.cid,CircleDef.subid==self_uc.subid)).first()
            if self_cd.level>to_set_cd.level:
                return Res(errno=2,error="can not lower level")
        self_uc=UserCircle()
        self_uc.uid=BackEndEnvData.uid
        self_uc.cid=data['cid']
        self_uc.subid=data['subid']
        self_uc.by_uid=data['uid']
        self_uc=session.merge(self_uc)
        session.commit()
        return Res({"circle":{"cid":self_uc.cid,"subid":self_uc.subid}})
