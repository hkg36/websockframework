from tools.session import CheckSession

__author__ = 'amen'
from datamodel.user_circle import CircleDef, UserCircle
from tools.helper import Res
import BackEndEnvData
import dbconfig

@CheckSession()
def run(cid,subid):
    if not cid or not subid:
        return Res(errno=3,error="cid and subid not be 0")
    with dbconfig.Session() as session:
        cdef=session.query(CircleDef).filter(CircleDef.cid==cid,CircleDef.subid==subid).first()
        if cdef is None:
            return Res(errno=3,error="not cid or not subid")
        uc=UserCircle()
        uc.uid=BackEndEnvData.uid
        uc.cid=cid
        uc.subid=subid
        session.merge(uc)
        session.commit()
        return Res({"title":cdef.title,"level":cdef.level})