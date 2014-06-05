#coding:utf-8
from sqlalchemy import and_
from datamodel.events import Events
from datamodel.friendlist import FriendList
from tools.addPushQueue import AddEventNotify
from tools.session import CheckSession, GenSession

__author__ = 'amen'
from datamodel.user_circle import CircleRole, UserCircle
from tools.helper import Res, DefJsonEncoder
import BackEndEnvData
import dbconfig
import json

@CheckSession()
def run(eid,roleid=None):
    with dbconfig.Session() as session:
        event=session.query(Events).filter(Events.eid==eid).first()
        if event is None or event.type!="request_join_circle":
            return Res(errno=3,error="not event")

        uid=event.param1
        cid=event.param2

        self_circle,self_role=session.query(UserCircle,CircleRole).join(CircleRole,and_(CircleRole.cid==UserCircle.cid,CircleRole.roleid==UserCircle.roleid)).\
            filter(UserCircle.cid==cid).first()
        if roleid is not None and roleid!=self_circle.roleid:
            toset_role=session.query(CircleRole).filter(and_(CircleRole.cid==cid,CircleRole.roleid==roleid)).first()
            if toset_role.level>self_role.level:
                return Res(errno=2,error="role level too height")
        else:
            toset_role=self_role

        self_uc=UserCircle()
        self_uc.uid=uid
        self_uc.cid=toset_role.cid
        self_uc.roleid=toset_role.roleid
        self_uc.by_uid=BackEndEnvData.uid
        self_uc=session.merge(self_uc)
        session.commit()

        #添加好友
        friend=FriendList()
        friend.uid=self_uc.uid
        friend.friendid=self_uc.by_uid
        friend.type=2
        friend1=session.merge(friend)
        friend=FriendList()
        friend.uid=self_uc.by_uid
        friend.friendid=self_uc.uid
        friend.type=2
        friend2=session.merge(friend)
        session.commit()
        #发送通知
        event=Events()
        event.touid=friend1.uid
        event.param1=friend1.friendid
        event.type="add_friend"
        event1=session.merge(event)
        event=Events()
        event.touid=friend1.friendid
        event.param1=friend1.uid
        event.type="add_friend"
        event2=session.merge(event)

        event=Events()
        event.touid=self_uc.uid
        event.param1=self_uc.cid
        event.param2=self_uc.roleid
        event.param3=self_uc.by_uid
        event.type="accept_join_circle"
        event3=session.merge(event)

        session.commit()
        AddEventNotify(event1)
        AddEventNotify(event2)
        AddEventNotify(event3)
        return Res()