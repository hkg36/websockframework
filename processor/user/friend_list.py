#coding:utf-8
from datamodel.friendlist import FriendList
from tools.helper import Res
from tools.session import CheckSession

__author__ = 'amen'
import BackEndEnvData
import dbconfig


@CheckSession()
def run(uid=0,pos=0,count=10):
    with dbconfig.Session() as session:
        allfriend=session.query(FriendList).filter(FriendList.uid==(BackEndEnvData.uid if uid==0 else uid))\
            .order_by(FriendList.time.desc())\
            .offset(pos).limit(count).all()
        fl=[]
        default_friend={
            24, #来信小助手
        }
        for one in allfriend:
            if one.friendid in default_friend:
                default_friend.remove(one.friendid)
            fl.append({'uid':one.friendid,'type':one.type,'time':one.time})
        for one in default_friend:
            fl.append({'uid':one,'type':0,'time':0})
    return Res({'friend_id':fl,'pos':pos,'count':count})