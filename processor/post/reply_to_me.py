#coding:utf-8
from sqlalchemy import and_
from datamodel.post import Post
from datamodel.post_reply import PostReply
from tools.addPushQueue import AddPostPublish
from tools.helper import Res
from tools.session import CheckSession

__author__ = 'amen'
import BackEndEnvData
import dbconfig

@CheckSession(level=0)
def run(from_reply=0):
    with dbconfig.Session() as session:
        reply_list=[]
        posts=session.query(Post).filter(Post.uid).order_by(Post.postid.desc()).limit(20).all()
        post_ids=[]
        for post in posts:
            post_ids.append(post.postid)

        subquery=session.query(PostReply)
        if from_reply:
            subquery=subquery.filter(and_(PostReply.postid.in_(post_ids),PostReply.replyid>from_reply))
        else:
            subquery=subquery.filter(PostReply.postid.in_(post_ids))
        replys=subquery.order_by(PostReply.replyid).limit(100).all()
        for reply in replys:
            reply_list.append(reply.toJson())
        return Res({"replys":reply_list})
