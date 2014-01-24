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
        post_ids=set()

        posts=session.query(Post).filter(Post.uid).order_by(Post.postid.desc()).limit(20).all()
        for post in posts:
            post_ids.add(post.postid)
        replys=session.query(PostReply).filter(PostReply.uid==BackEndEnvData.uid).order_by(PostReply.replyid.desc()).limit(30).all()
        for reply in replys:
            post_ids.add(reply.postid)

        subquery=session.query(PostReply)
        subquery=subquery.filter(and_(PostReply.postid.in_(list(post_ids)),PostReply.replyid>from_reply))
        replys=subquery.order_by(PostReply.replyid).limit(100).all()
        for reply in replys:
            reply_list.append(reply.toJson())
        return Res({"replys":reply_list})
