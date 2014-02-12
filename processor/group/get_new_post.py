#coding:utf-8
from sqlalchemy import and_

from datamodel.post import Post
from tools.helper import Res
from tools.session import CheckSession


__author__ = 'amen'
import dbconfig
@CheckSession()
def run(gid,frompos):
    with dbconfig.Session() as session:
        posts=session.query(Post).filter(and_(Post.group_id==gid,Post.postid>frompos)).order_by(Post.postid.desc()).all()
        plist=[]
        for post in posts:
            pdata=post.toJson()
            pdata['ilike']=False
            plist.append(pdata)
    return Res({'posts':plist})
