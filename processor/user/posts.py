#coding:utf-8
from sqlalchemy import and_
from datamodel.post import Post
from tools.helper import Res
from tools.session import CheckSession
import BackEndEnvData
import dbconfig
import json
@CheckSession()
def run(uid,before=None,count=None):
    with dbconfig.Session() as session:
        query=session.query(Post)
        if before is None:
            query=query.filter(Post.uid==uid)
        else:
            query=query.filter(and_(Post.uid==uid,Post.postid<before))
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