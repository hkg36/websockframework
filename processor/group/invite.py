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
        if group is None or (group.everyone_caninvite==0 and group.creator!=BackEndEnvData.uid):
            return Res(errno=2,error="not everyone can invaite and you are not creator")
        if group.creator!=uid:
            gm=session.query(GroupMember).filter(and_(GroupMember.gid==gid,GroupMember.uid==uid)).first()
            if gm is None:
                return Res(errno=2,error="you are not member")

        events=[]
        for u in uid:
            event=Events()
            event.touid=u
            event.type="group_invite"
            event.param1=gid
            event.param2=BackEndEnvData.uid
            event=session.merge(event)
            events.append(event)
        session.commit()
        for ev in events:
            AddEventNotify(ev)
    return Res()