from sqlalchemy import and_
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
    session.query(FriendList).filter(and_(FriendList.uid==BackEndEnvData.uid,
                                          FriendList.friendid.in_(uid))).delete('fetch')
    session.commit()
    return Res()