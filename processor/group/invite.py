#coding:utf-8
from datamodel.events import Events
from datamodel.group import Group
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