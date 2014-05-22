from tools.session import CheckSession

__author__ = 'amen'
from datamodel.user_circle import CircleDef, UserCircle, CircleBoardHistory
from tools.helper import Res
import BackEndEnvData
import dbconfig

def run(cid):
    with dbconfig.Session() as session:
        cbhs=session.query(CircleBoardHistory).filter(CircleBoardHistory.cid==cid).order_by(CircleBoardHistory.time.desc()).all()
        cblist=[]
        for one in cbhs:
            cblist.append(one.toJson())
        return Res({"boards":cblist})
