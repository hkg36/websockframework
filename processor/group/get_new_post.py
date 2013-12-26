from sqlalchemy import and_
from datamodel.post import Post
from datamodel.post_like import PostLike
from tools.helper import Res, GetFileLink
from tools.session import CheckSession

__author__ = 'amen'
import BackEndEnvData
import dbconfig
@CheckSession
def run(gid,frompos):
    session=dbconfig.Session()
    posts=session.query(Post).filter(and_(Post.group_id==gid,Post.postid>frompos)).order_by(Post.postid.desc()).all()
    plist=[]
    for post in posts:
        pdata=post.toJson()
        pdata['ilike']=False
        plist.append(pdata)
    session.close()
    return Res({'posts':plist})
