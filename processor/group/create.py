from datamodel.group import Group
from datamodel.group_member import GroupMember
from tools.helper import Res
from tools.session import CheckSession

__author__ = 'amen'
import BackEndEnvData
import dbconfig
@CheckSession
def run(name,board,type=0):
    session=dbconfig.Session()
    newgroup=Group()
    newgroup.creator=BackEndEnvData.uid
    newgroup.group_name=name
    newgroup.group_board=board
    newgroup.type=type
    newgroup=session.merge(newgroup)
    session.flush()
    gmember=GroupMember()
    gmember.gid=newgroup.gid
    gmember.uid=BackEndEnvData.uid
    gmember.type=0
    session.merge(gmember)
    session.commit()
    return Res({'gid':newgroup.gid})