#coding:utf-8
from datamodel.post2 import GroupPost
from datamodel.user_circle import LikeRecord
from tools.helper import Res, DefJsonEncoder
from tools.session import CheckSession, FrequencyControl


__author__ = 'amen'
import BackEndEnvData
import dbconfig

@CheckSession()
@FrequencyControl()
def run(postid):
    post=GroupPost.objects(postid=postid).first()
    if post is None:
        return Res(errno=3,error="post not exists")
    for one in post.likes:
        if one.uid==BackEndEnvData.uid:
            return Res({'like':one.toJson()})
    newlike=LikeRecord()
    newlike.uid=BackEndEnvData.uid
    post.likes.append(newlike)
    post.save()

    json_msg=DefJsonEncoder.encode({"like":newlike.toJson(),"postid":post.postid,"gid":post.gid})
    BackEndEnvData.queue_producer.publish(body=json_msg,
                                        headers={"uid":post.uid,"type":"group.post.newlike"},
                                        delivery_mode=2,
                                        routing_key='sys.push_to_user',
                                        compression='gzip')
    return Res({'like':newlike.toJson()})