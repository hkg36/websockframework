from datamodel.events import Events
from datamodel.message import Message
from datamodel.post import Post
from datamodel.post_like import PostLike
from datamodel.post_reply import PostReply

__author__ = 'amen'
import dbconfig
import datetime


def DataClean():
    deadline=datetime.datetime.now()-datetime.timedelta(days=60)
    with dbconfig.Session() as session:
        msg_deleted=session.query(Message).filter(Message.time<deadline).delete(False)
        event_deleted=session.query(Events).filter(Events.create_time<deadline).delete(False)

        todelete_post=session.query(Post.postid).filter(Post.time<deadline).subquery()
        post_like_deleted=session.query(PostLike).filter(PostLike.postid.in_(todelete_post)).delete(False)
        post_reply_deleted=session.query(PostReply).filter(PostReply.postid.in_(todelete_post)).delete(False)
        post_deleted=session.query(Post).filter(Post.time<deadline).delete(False)
        session.commit()
        print "del %d msg,%d event,%d post,%d postlike,%d postreply"%(msg_deleted,event_deleted,post_deleted,post_like_deleted,post_reply_deleted)

if __name__ == '__main__':
    DataClean()

