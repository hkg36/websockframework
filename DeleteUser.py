from sqlalchemy import or_
from datamodel.events import Events
from datamodel.friendlist import FriendList
from datamodel.group_member import GroupMember
from datamodel.message import Message
from datamodel.post import Post
from datamodel.post2 import GroupPost
from datamodel.post_like import PostLike
from datamodel.post_reply import PostReply
from datamodel.user import User
from datamodel.user_circle import UserCircle, CirclePost
import dbconfig
import time
import datetime
import sys

def CleanUser(uids):
    uids=list(uids)
    #CirclePost.objects(uid__in=uids).delete()
    #GroupPost.objects(uid__in=uids).delete()
    with dbconfig.Session() as session:
        msg_deleted=session.query(Message).filter(or_(Message.toid.in_(uids),Message.fromid.in_(uids))).delete(False)
        event_deleted=session.query(Events).filter(Events.touid.in_(uids)).delete(False)

        todelete_post=session.query(Post.postid).filter(Post.uid.in_(uids)).subquery()
        post_like_deleted=session.query(PostLike).filter(PostLike.postid.in_(todelete_post)).delete(False)
        post_reply_deleted=session.query(PostReply).filter(PostReply.postid.in_(todelete_post)).delete(False)
        post_deleted=session.query(Post).filter(Post.uid.in_(uids)).delete(False)
        session.query(UserCircle).filter(UserCircle.uid.in_(uids)).delete(False)
        session.query(GroupMember).filter(GroupMember.uid.in_(uids)).delete(False)
        session.query(FriendList).filter(or_(FriendList.uid.in_(uids),FriendList.friendid.in_(uids))).delete(False)

        session.query(User).filter(User.uid.in_(uids)).delete(False)
        session.commit()

if __name__ == '__main__':
    uids=[int(one) for one in sys.argv[1:]]
    if len(uids)==0:
        exit()
    print "delete user:",uids
    CleanUser(uids)