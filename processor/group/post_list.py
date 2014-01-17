from sqlalchemy import and_
from datamodel.post import Post
from datamodel.post_like import PostLike
from tools.helper import Res, GetFileLink
from tools.session import CheckSession

__author__ = 'amen'
import BackEndEnvData
import dbconfig

@CheckSession
def run(gid,pos=0,count=50):
    with dbconfig.Session() as session:
        query=session.query(Post).filter(Post.group_id==gid).order_by(Post.postid.desc())
        if pos>0:
            query=query.offset(pos)
        query=query.limit(count)
        posts=query.all()
        plist=[]
        for post in posts:
            pdata=post.toJson()
            ilike_record=session.query(PostLike).filter(and_(PostLike.postid==post.postid,PostLike.uid==BackEndEnvData.uid)).first()
            pdata['ilike']=True if ilike_record is not None else False
            plist.append(pdata)
        return Res({'posts':plist})