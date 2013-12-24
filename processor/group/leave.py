from sqlalchemy import and_
from datamodel.group_member import GroupMember
from tools.helper import Res
from tools.session import CheckSession

__author__ = 'amen'
import BackEndEnvData
import dbconfig
import anyjson
@CheckSession
def run(gid):
    session=dbconfig.Session()
    session.query(GroupMember).filter(and_(GroupMember.gid==gid,GroupMember.uid==BackEndEnvData.uid)).delete()
    session.commit()
    return Res()