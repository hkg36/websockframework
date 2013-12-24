from datamodel.friendlist import FriendList
from datamodel.user import User
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
    users=session.query(User).filter(User.uid.in_(uid)).all()
    ulist=[]
    for user in users:
        ulist.append(user.toJson())
    return Res({"users":ulist})