from datamodel.post import Post
from datamodel.post_reply import PostReply
from tools.helper import Res
from tools.session import CheckSession

__author__ = 'amen'
import BackEndEnvData
import dbconfig
@CheckSession
def run(postid,content):
    session=dbconfig.Session()
    newreply=PostReply()
    newreply.postid=postid
    newreply.uid=BackEndEnvData.uid
    newreply.content=content
    newreply=session.merge(newreply)
    session.flush()
    newreplyid=newreply.replyid
    session.query(Post).filter(Post.postid==postid).update({Post.replycount:Post.replycount+1})
    session.commit()
    session.close()
    return Res({"replyid":newreplyid})