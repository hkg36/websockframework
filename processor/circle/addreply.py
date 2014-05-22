from tools.session import CheckSession

__author__ = 'amen'
from datamodel.user_circle import CircleDef, UserCircle, CircleBoardHistory, CirclePost, ReplyRecord
from tools.helper import Res
import BackEndEnvData
import dbconfig

@CheckSession()
def run(postid,content):
    newpost=CirclePost.objects(postid=postid).first()
    newreply=ReplyRecord()
    newreply.uid=BackEndEnvData.uid
    newreply.content=content
    newpost.replys.append(newreply)
    newpost.save()
    return Res({"post":newreply.toJson()})
