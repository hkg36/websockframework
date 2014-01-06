from datamodel.events import Events
from datamodel.group import Group
from tools.addPushQueue import AddEventNotify
from tools.helper import Res
from tools.session import CheckSession

__author__ = 'amen'
import BackEndEnvData
import dbconfig
@CheckSession
def run(gid,uid):
    with dbconfig.Session() as session:
        event=Events()
        event.touid=uid
        event.type="group_invite"
        event.param1=gid
        event.param2=BackEndEnvData.uid
        event=session.merge(event)
        session.commit()
        AddEventNotify(event)
    return Res()