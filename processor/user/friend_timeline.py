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
def run(before=None,count=None):
    with dbconfig.Session() as session:
        allfriend=session.query(FriendList).filter(FriendList.uid==BackEndEnvData.uid).all()
        fl=[]
        for one in allfriend:
            fl.append(one.friendid)

        query=session.query(Post)
        if before is None:
            query=query.filter(Post.uid.in_(fl))
        else:
            query=query.filter(and_(Post.uid.in_(fl),Post.postid<before))
        query=query.order_by(Post.postid.desc())
        if count is None:
            query=query.limit(50)
        else:
            query=query.limit(min(500,int(count)))
        posts=query.all()
        postlist=[]
        for p in posts:
            postlist.append(p.toJson())
        return Res({"posts":postlist})
