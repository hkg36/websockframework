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
def run(uid,cid):
    if uid==BackEndEnvData.uid:
        return Res(errno=2,error="not self invite")
    with dbconfig.Session() as session:
        findparam=UserCircle.uid==uid
        findparam=and_(findparam,UserCircle.cid==cid)
        by_user_c=session.query(UserCircle).filter(findparam).order_by(UserCircle.time).first()
        if by_user_c is None:
            return Res(errno=3,error="user not in any circle")
        self_uc=session.query(UserCircle).filter(and_(UserCircle.uid==BackEndEnvData.uid,UserCircle.cid==by_user_c.cid)).first()
        if self_uc:
            return Res({"circle":{"cid":self_uc.cid,"roleid":self_uc.roleid}})

        new_event=Events()
        new_event.type="request_join_circle"
        new_event.param1=BackEndEnvData.uid
        new_event.param2=cid
        new_event.touid=uid
        new_event=session.merge(new_event)
        session.commit()

        AddEventNotify(new_event)

        return Res()