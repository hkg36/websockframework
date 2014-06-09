from tools.session import CheckSession

__author__ = 'amen'
from datamodel.user_circle import CircleDef,CircleRole, UserCircle
from tools.helper import Res
import BackEndEnvData
import dbconfig

@CheckSession()
def run(cid):
    with dbconfig.Session() as session:
        session.query(UserCircle).filter(UserCircle.cid==cid,UserCircle.uid==BackEndEnvData.uid).delete()
        session.commit()
    return Res()
