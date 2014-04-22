#coding:utf-8
from datamodel.events import Events
from datamodel.friendlist import FriendList
from datamodel.user import User
from tools.addPushQueue import AddEventNotify
from tools.helper import Res
from tools.session import CheckSession

__author__ = 'amen'
import BackEndEnvData
import dbconfig
import datetime

@CheckSession()
def run(active_code):
    actinfo=dbconfig.memclient.get(("active_code:%s"%active_code).encode('utf-8'))
    if actinfo is None:
        return Res({},3,"not active code")
    if actinfo['uid']==BackEndEnvData.uid:
        return Res({},3,"do not self active")
    with dbconfig.Session() as session:
        user=session.query(User).filter(User.uid==BackEndEnvData.uid).first()
        user.actor=1
        user.active_by=actinfo['uid']
        user.active_level=actinfo['level']
        user.active_time=datetime.datetime.now()
        user=session.merge(user)
        session.commit()
        #添加好友
        friend=FriendList()
        friend.uid=BackEndEnvData.uid
        friend.friendid=user.active_by
        friend.type=2
        friend1=session.merge(friend)
        friend=FriendList()
        friend.uid=user.active_by
        friend.friendid=BackEndEnvData.uid
        friend.type=2
        friend2=session.merge(friend)
        session.commit()
        #发送通知
        event=Events()
        event.touid=user.active_by
        event.param1=BackEndEnvData.uid
        event.type="add_friend"
        event1=session.merge(event)
        event=Events()
        event.touid=BackEndEnvData.uid
        event.param1=user.active_by
        event.type="add_friend"
        event2=session.merge(event)
        session.commit()
        AddEventNotify(event1)
        AddEventNotify(event2)

        return Res({'active_level':user.active_level,'active_by':user.active_by})