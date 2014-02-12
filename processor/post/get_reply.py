#coding:utf-8
from datamodel.post_reply import PostReply
from tools.helper import Res
from tools.session import CheckSession

__author__ = 'amen'
import dbconfig

@CheckSession()
def run(postid,pos=0,count=20):
    with dbconfig.Session() as session:
        replys=session.query(PostReply).filter(PostReply.postid==postid).offset(pos).limit(count).all()
        rplist=[]
        for reply in replys:
            rplist.append(reply.toJson())
        return Res({'replys':rplist})