from datamodel.friendlist import FriendList
from tools.helper import Res
from tools.session import CheckSession

__author__ = 'amen'
import BackEndEnvData
import dbconfig
import anyjson
@CheckSession
def run(uid):
    if isinstance(uid,list)==False:
        uid=[uid]
    session=dbconfig.Session()
    for id in uid:
        if id!=BackEndEnvData.uid:
            friend=FriendList()
            friend.uid=BackEndEnvData.uid
            friend.friendid=id
            session.merge(friend)
    session.commit()
    return Res()