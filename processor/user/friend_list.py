from datamodel.friendlist import FriendList
from tools.helper import Res
from tools.session import CheckSession

__author__ = 'amen'
import BackEndEnvData
import dbconfig
import anyjson
import time
@CheckSession
def run(uid=0,pos=0,count=10):
    with dbconfig.Session() as session:
        allfriend=session.query(FriendList).filter(FriendList.uid==(BackEndEnvData.uid if uid==0 else uid))\
            .order_by(FriendList.time.desc())\
            .offset(pos).limit(count).all()
        fl=[]
        for one in allfriend:
            fl.append({'uid':one.friendid,'type':one.type,'time':one.time})
    return Res({'friend_id':fl,'pos':pos,'count':count})