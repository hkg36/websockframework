#coding:utf-8
from sqlalchemy import and_
from datamodel.group import Group
from datamodel.group_member import GroupMember
from tools.helper import Res, CombineGeo
from tools.session import CheckSession

__author__ = 'amen'
import BackEndEnvData
import dbconfig
@CheckSession()
def run(gid,uid,can_post=None):
    with dbconfig.Session() as session:
        group=session.query(Group).filter(Group.gid==gid).first()
        if group is None or group.creator!=BackEndEnvData.uid:
            return Res(errno=2,error='group not exist or you not right')
        groupmember=session.query(GroupMember).filter(and_(GroupMember.gid==gid,GroupMember.uid==uid)).first()
        if groupmember is None:
            return Res(errno=2,error='not member in group')
        if can_post is not None:
            groupmember.can_post=can_post
        groupmember=session.merge(groupmember)
        session.commit()
        return Res()