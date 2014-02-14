#coding:utf-8
from sqlalchemy import and_

from datamodel.friendlist import FriendList
from datamodel.post import Post
from tools.helper import Res
from tools.session import CheckSession


__author__ = 'amen'
import BackEndEnvData
import dbconfig


@CheckSession()
def run(after):
    with dbconfig.Session() as session:
        allfriend=session.query(FriendList).filter(FriendList.uid==BackEndEnvData.uid).all()
        fl=[]
        for one in allfriend:
            fl.append(one.friendid)

        query=session.query(Post).filter(and_(Post.uid.in_(fl),Post.postid>after))
        query=query.order_by(Post.postid.desc())
        query=query.limit(500)
        posts=query.all()
        postlist=[]
        for p in posts:
            postlist.append(p.toJson())
        return Res({"posts":postlist})
