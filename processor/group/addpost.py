#coding:utf-8
from datamodel.post2 import GroupPost
from tools.helper import Res, DefJsonEncoder
from tools.session import CheckSession


__author__ = 'amen'
import BackEndEnvData
import dbconfig

@CheckSession()
def run(gid,content=None,pictures=[],video=None,videolen=None,voice=None,voicelen=None,
    lat=None,lng=None):
    if not content and not pictures and not video and not voice:
        return Res(errno=2,error="not conent is not allow")
    newpost=GroupPost()
    newpost.gid=gid
    newpost.uid=BackEndEnvData.uid
    if content:
        newpost.content=content
    if pictures:
        newpost.pictures=pictures
    if video:
        newpost.video=video
        newpost.voicelen=videolen
    if voice:
        newpost.voice=voice
        newpost.voicelen=voicelen
    if lat is not None and lng is not None:
        newpost.position=[lng,lat]
    newpost.save()

    json_msg=DefJsonEncoder.encode(newpost.toJson())
    BackEndEnvData.queue_producer.publish(body=json_msg,delivery_mode=2,
                                        routing_key="group.change",headers={"type":"group.newpost"},
                                        compression='gzip')

    return Res({'postid':newpost.postid})
