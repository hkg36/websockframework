from datamodel.post import Post
from datamodel.post_reply import PostReply
from tools.addPushQueue import AddReplyNotify
from tools.helper import Res
from tools.session import CheckSession

__author__ = 'amen'
import BackEndEnvData
import dbconfig
@CheckSession
def run(postid,content):
    with dbconfig.Session() as session:
        newreply=PostReply()
        newreply.postid=postid
        newreply.uid=BackEndEnvData.uid
        newreply.content=content
        newreply=session.merge(newreply)
        session.query(Post).filter(Post.postid==postid).update({Post.replycount:Post.replycount+1})
        session.commit()
        AddReplyNotify(newreply)
        return Res({"replyid":newreply.replyid})