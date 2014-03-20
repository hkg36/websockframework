#coding:utf-8
import datetime
from sqlalchemy import and_

from datamodel.post import Post
from datamodel.post_like import PostLike
from datamodel.post_reply import PostReply
from tools.helper import Res
from tools.session import CheckSession


__author__ = 'amen'
import BackEndEnvData
import dbconfig

@CheckSession(level=0)
def run(from_reply=0,like_after=None):
    with dbconfig.Session() as session:

        post_ids=set()

        posts=session.query(Post).filter(Post.uid).order_by(Post.postid.desc()).limit(20).all()
        for post in posts:
            post_ids.add(post.postid)
        replys=session.query(PostReply).filter(PostReply.uid==BackEndEnvData.uid).order_by(PostReply.replyid.desc()).limit(30).all()
        for reply in replys:
            post_ids.add(reply.postid)

        result={}
        if len(post_ids)==0:
            result["replys"]=[]
        else:
            reply_list=[]
            subquery=session.query(PostReply)
            subquery=subquery.filter(and_(PostReply.postid.in_(list(post_ids)),PostReply.replyid>from_reply))
            replys=subquery.order_by(PostReply.replyid).limit(100).all()
            for reply in replys:
                reply_list.append(reply.toJson())
            result["replys"]=reply_list
        if like_after is not None:
            likes=session.query(PostLike).filter(and_(PostLike.postid.in_(list(post_ids)),PostLike.time>datetime.datetime.fromtimestamp(like_after))).order_by(PostLike.time.desc()).limit(50).all()
            likelist=[]
            for like in likes:
                likelist.append(like.toJson())
            result['likes']=likelist
        return Res(result)
