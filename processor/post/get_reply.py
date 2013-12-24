from datamodel.post import Post
from datamodel.post_reply import PostReply
from tools.helper import Res
from tools.session import CheckSession

__author__ = 'amen'
import BackEndEnvData
import dbconfig
def ReplyToJson(reply):
    return {
        "replyid":reply.replyid,
		"postid":reply.postid,
		"uid":reply.uid,
		"content":reply.content,
		"time":reply.time
    }
@CheckSession
def run(postid,pos=0,count=20):
    session=dbconfig.Session()
    replys=session.query(PostReply).filter(PostReply.postid==postid).offset(pos).limit(count).all()
    rplist=[]
    for reply in replys:
        rplist.append(ReplyToJson(reply))
    session.close()
    return Res({'replys':rplist})