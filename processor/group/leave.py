#coding:utf-8
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
    with dbconfig.Session() as session:
        session.query(GroupMember).filter(and_(GroupMember.gid==gid,GroupMember.uid==BackEndEnvData.uid)).delete()
        session.commit()
    return Res()