#coding:utf-8
from datamodel.events import Events
from datamodel.friendlist import FriendList
from tools.addPushQueue import AddEventNotify
from tools.helper import Res
from tools.session import CheckSession

__author__ = 'amen'
import BackEndEnvData
import dbconfig
import anyjson
@CheckSession()
def run(uid,type=0):
    if isinstance(uid,list)==False:
        uid=[uid]
    uids=[]
    for u in uid:
        if u!=BackEndEnvData.uid:
            uids.append(u)
    with dbconfig.Session() as session:
        eventpost=[]
        for id in uids:
            friend=FriendList()
            friend.uid=BackEndEnvData.uid
            friend.friendid=id
            friend.type=type
            session.merge(friend)

            event=Events()
            event.touid=id
            event.param1=BackEndEnvData.uid
            event.type="add_friend"
            event=session.merge(event)
            eventpost.append(event)

        session.commit()
        for e in eventpost:
            AddEventNotify(e)
    return Res()