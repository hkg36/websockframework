from datamodel.group import Group
from datamodel.group_member import GroupMember
from tools.helper import Res
from tools.session import CheckSession

__author__ = 'amen'
import BackEndEnvData
import dbconfig
@CheckSession
def run(gid,name=None,board=None,type=0):
    with dbconfig.Session() as session:
        ginfo=session.query(Group).filter(Group.gid==gid).first()
        if ginfo is None:
            return Res({},2,"group not exists")
        if ginfo.creator!=BackEndEnvData.uid:
            return Res({},2,'not creator')
        if name:
            ginfo.group_name = name
        if board:
            ginfo.group_board = board
        if type:
            ginfo.type = type
        session.merge(ginfo)
        session.commit()

        return Res()
