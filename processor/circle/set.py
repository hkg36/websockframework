from tools.session import CheckSession

__author__ = 'amen'
from datamodel.user_circle import CircleDef,CircleRole, UserCircle
from tools.helper import Res
import BackEndEnvData
import dbconfig

@CheckSession()
def run(cid,roleid):
    if not cid or not roleid:
        return Res(errno=3,error="cid and subid not be 0")
    with dbconfig.Session() as session:
        crole=session.query(CircleRole).filter(CircleRole.cid==cid,CircleRole.roleid==roleid).first()
        if crole is None:
            return Res(errno=3,error="not cid or not roleid")
        uc=UserCircle()
        uc.uid=BackEndEnvData.uid
        uc.cid=cid
        uc.roleid=roleid
        session.merge(uc)
        session.commit()
        return Res({"role":crole.toJson()})