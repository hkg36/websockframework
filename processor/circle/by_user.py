#coding:utf-8
from sqlalchemy import and_
from datamodel.events import Events
from datamodel.friendlist import FriendList
from tools.addPushQueue import AddEventNotify
from tools.session import CheckSession, GenSession

__author__ = 'amen'
from datamodel.user_circle import CircleRole, UserCircle, CircleDef
from tools.helper import Res, DefJsonEncoder
import BackEndEnvData
import dbconfig
import json

@CheckSession()
def run(uid,cid=None):
    if uid==BackEndEnvData.uid:
        return Res(errno=2,error="not self invite")
    with dbconfig.Session() as session:
        findparam=UserCircle.uid==uid
        if cid != None:
            findparam=and_(findparam,UserCircle.cid==cid)
        by_user_c=session.query(UserCircle).filter(findparam).order_by(UserCircle.time).first()
        if by_user_c is None:
            return Res(errno=3,error="user not in any circle")
        cdef=session.query(CircleDef).filter(CircleDef.cid==by_user_c.cid).first()

        self_uc=UserCircle()
        self_uc.uid=BackEndEnvData.uid
        self_uc.cid=by_user_c.cid
        self_uc.roleid=cdef.default_roleid
        self_uc.by_uid=by_user_c.uid
        self_uc=session.merge(self_uc)
        session.commit()

        #添加好友
        friend=FriendList()
        friend.uid=BackEndEnvData.uid
        friend.friendid=self_uc.by_uid
        friend.type=2
        friend1=session.merge(friend)
        friend=FriendList()
        friend.uid=self_uc.by_uid
        friend.friendid=BackEndEnvData.uid
        friend.type=2
        friend2=session.merge(friend)
        session.commit()
        #发送通知
        event=Events()
        event.touid=self_uc.by_uid
        event.param1=BackEndEnvData.uid
        event.type="add_friend"
        event1=session.merge(event)
        event=Events()
        event.touid=BackEndEnvData.uid
        event.param1=self_uc.by_uid
        event.type="add_friend"
        event2=session.merge(event)
        session.commit()
        AddEventNotify(event1)
        AddEventNotify(event2)

        return Res({"circle":{"cid":self_uc.cid,"roleid":self_uc.roleid}})