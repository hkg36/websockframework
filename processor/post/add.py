#coding:utf-8
from sqlalchemy import and_
from datamodel.group import Group
from datamodel.group_member import GroupMember
from datamodel.post import Post
from tools.addPushQueue import AddPostPublish
from tools.helper import Res
from tools.session import CheckSession

__author__ = 'amen'
import BackEndEnvData
import dbconfig

@CheckSession(level=0)
def run(gid,content):
    with dbconfig.Session() as session:
        ginfo=session.query(Group).filter(Group.gid==gid).first()
        if ginfo is None:
            return Res({},2,"group not exists")
        if ginfo.only_member_speak and ginfo.creator!=BackEndEnvData.uid:
            member=session.query(GroupMember).filter(and_(GroupMember.gid==gid,GroupMember.uid==BackEndEnvData.uid)).first()
            if member is None:
                return Res(errno=2,error="only member can speak")
        newpost=Post()
        newpost.uid=BackEndEnvData.uid
        newpost.group_id=gid
        newpost.content=content
        newpost=session.merge(newpost)
        session.commit()
        AddPostPublish(newpost.toJson())
        return Res({'postid':newpost.postid})