from datamodel.group_member import GroupMember
from tools.helper import Res
from tools.session import CheckSession

__author__ = 'amen'
import BackEndEnvData
import dbconfig
@CheckSession
def run():
    session=dbconfig.Session()
    gms=session.query(GroupMember).filter(GroupMember.uid==BackEndEnvData.uid).all()
    glist=[]
    for gm in gms:
        glist.append({'gid':gm.gid,'type':gm.type,'time':gm.time})
    session.close()
    return Res({'groups':glist})