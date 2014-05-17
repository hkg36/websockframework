from datamodel.user_circle import CircleDef,CircleRole
from tools.helper import Res

__author__ = 'amen'
import BackEndEnvData
import dbconfig

def run(cid):
    with dbconfig.Session() as session:
        circle=session.query(CircleDef).filter(CircleDef.cid==cid).first()
        roles=session.query(CircleRole).filter(CircleRole.cid==cid).all()
        cl=[]
        for c in roles:
            cl.append(c.toJson())
        return Res({"circle":circle.toJson(),'roles':cl})
