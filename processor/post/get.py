#coding:utf-8
from sqlalchemy import and_
from datamodel.post import Post
from datamodel.post_like import PostLike
from tools.helper import Res, GetFileLink
from tools.session import CheckSession

__author__ = 'amen'
import BackEndEnvData
import dbconfig

@CheckSession
def run(postid):
    if isinstance(postid,list)==False:
        postid=[postid]
    with dbconfig.Session() as session:
        posts=session.query(Post).filter(Post.postid.in_(postid)).all()
        plist=[]
        for post in posts:
            pdata=post.toJson()
            ilike_record=session.query(PostLike).filter(and_(PostLike.postid==post.postid,PostLike.uid==BackEndEnvData.uid)).first()
            pdata['ilike']=True if ilike_record is not None else False
            plist.append(pdata)
        return Res({'posts':plist})
