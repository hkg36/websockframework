from datamodel.user_circle import CircleDef
from tools.helper import Res

__author__ = 'amen'
import BackEndEnvData
import dbconfig

def run(cid):
    with dbconfig.Session() as session:
        circles=session.query(CircleDef).filter(CircleDef.cid==cid).all()
        cl=[]
        for c in circles:
            cl.append({"cid":c.cid,"subid":c.subid,"title":c.title,"level":c.level})
        return Res({"circle":cl})
