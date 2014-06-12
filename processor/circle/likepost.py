#coding:utf-8
from tools.session import CheckSession

__author__ = 'amen'
from datamodel.user_circle import CircleDef, UserCircle, CircleBoardHistory, CirclePost, LikeRecord
from tools.helper import Res, DefJsonEncoder
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

    json_msg=DefJsonEncoder.encode({"like":newlike.toJson(),"postid":post.postid,"cid":post.cid})
    BackEndEnvData.queue_producer.publish(body=json_msg,
                                        headers={"uid":post.uid,"type":"circle.post.newlike"},
                                        delivery_mode=2,
                                        routing_key='sys.push_to_user',
                                        compression='gzip')

    return Res({'like':newlike.toJson()})