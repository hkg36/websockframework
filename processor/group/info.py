from datamodel.group import Group
from tools.helper import Res
from tools.session import CheckSession

__author__ = 'amen'
import BackEndEnvData
import dbconfig
@CheckSession
def run(gid):
    if isinstance(gid,list)==False:
        gid=[gid]
    session=dbconfig.Session()
    gps=session.query(Group).filter(Group.gid.in_(gid)).all()
    glist=[]
    for gp in gps:
        glist.append(gp.toJson())
    session.close()
    return Res({"groups":glist})