from sqlalchemy import and_
from datamodel.post import Post
from datamodel.post_like import PostLike
from tools.helper import Res
from tools.session import CheckSession

__author__ = 'amen'
import BackEndEnvData
import dbconfig
import anyjson
@CheckSession
def run(postid):
    with dbconfig.Session() as session:
        likerecord=session.query(PostLike).filter(and_(PostLike.postid==postid,PostLike.uid==BackEndEnvData.uid)).first()
        if likerecord is not None:
            session.delete(likerecord)
            session.query(Post).filter(Post.postid==postid).update({Post.like:Post.like-1})
            session.commit()
    return Res()
