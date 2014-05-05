from tools.session import CheckSession

__author__ = 'amen'
from datamodel.user_circle import CircleDef, UserCircle
from tools.helper import Res
import BackEndEnvData
import dbconfig

@CheckSession()
def run(cid):
    with dbconfig.Session() as session:
        ucall=session.query(UserCircle).filter(UserCircle.cid==cid).order_by(UserCircle.time.desc()).all()
        ucl=[]
        for uc in ucall:
            ucl.append({"uid":uc.uid,"subid":uc.subid,'time':uc.time})
        return Res({"users":ucl})