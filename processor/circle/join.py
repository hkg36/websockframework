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
        cdef=session.query(CircleDef).filter(CircleDef.cid==data['cid']).first()
        self_uc=UserCircle()
        self_uc.uid=BackEndEnvData.uid
        self_uc.cid=data['cid']
        self_uc.roleid=cdef.default_roleid
        self_uc.by_uid=data['uid']
        self_uc=session.merge(self_uc)
        session.commit()
        return Res({"circle":{"cid":self_uc.cid,"roleid":self_uc.roleid}})
