#coding:utf-8
from tools.session import CheckSession

__author__ = 'amen'
from datamodel.user_circle import CircleDef, UserCircle, CircleBoardHistory, CirclePost, LikeRecord
from tools.helper import Res
import BackEndEnvData
import dbconfig

@CheckSession()
def run(postid):
    post=CirclePost.objects(postid=postid).first()
    for one in post.likes:
        if one.uid==BackEndEnvData.uid:
            return Res({'like':one.toJson()})
    newlike=LikeRecord()
    newlike.uid=BackEndEnvData.uid
    post.likes.append(newlike)
    post.save()
    return Res({'like':newlike.toJson()})