#coding:utf-8
from datamodel.post import Post
from datamodel.post_like import PostLike
from datamodel.post_reply import PostReply
from tools.helper import Res
from tools.session import CheckSession

__author__ = 'amen'
import BackEndEnvData
import dbconfig

@CheckSession
def run(postid):
    with dbconfig.Session() as session:
        post=session.query(Post).filter(Post.postid==postid).first()
        if post:
            if post.uid!=BackEndEnvData.uid:
                return Res(errno=2,error="not creator")
            session.delete(post)
            session.query(PostLike).filter(PostLike.postid==postid).delete()
            session.query(PostReply).filter(PostReply.postid==postid).delete()
            session.commit()
        else:
            return Res(errno=3,error="not exist")
        return Res()
