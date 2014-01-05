#coding:utf-8
from datamodel.group import Group
from datamodel.group_member import GroupMember
from tools.helper import Res
from tools.session import CheckSession

__author__ = 'amen'
import BackEndEnvData
import dbconfig
@CheckSession
def run(gid):
    with dbconfig.Session() as session:
        group_to_del=session.query(Group).filter(Group.gid==gid).first()
        if group_to_del.creator!=BackEndEnvData.uid:
            return Res(errno=2,error="group is not yours")
        session.delete(group_to_del)
        session.query(GroupMember).filter(GroupMember.gid==group_to_del.gid).delete()
        session.commit()
        return Res()
