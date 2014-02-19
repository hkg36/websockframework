#coding:utf-8
from sqlalchemy import and_
from datamodel.events import Events
from datamodel.group import Group
from datamodel.group_member import GroupMember
from tools.addPushQueue import AddEventNotify
from tools.helper import Res
from tools.session import CheckSession

__author__ = 'amen'
import BackEndEnvData
import dbconfig
@CheckSession()
def run(gid,uid):
    if isinstance(uid,list)==False:
        uid=[uid]
    with dbconfig.Session() as session:
        group=session.query(Group).filter(Group.gid==gid).first()
        if group is None or group.creator!=BackEndEnvData.uid:
            return Res(errno=2,error='group not exist or you not right')
        session.query(GroupMember).query(and_(GroupMember.gid==gid,GroupMember.uid.in_(uid))).delete()
        session.commit()
    return Res()
