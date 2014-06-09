from tools.session import CheckSession

__author__ = 'amen'
from datamodel.user_circle import CircleDef, UserCircle, CircleBoardHistory, CirclePost, ReplyRecord
from tools.helper import Res, DefJsonEncoder
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

    json_msg=DefJsonEncoder.encode({"reply":newreply.toJson(),
                                                        "postid":postid,
                                                        "cid":newpost.cid})
    BackEndEnvData.queue_producer.publish(body=json_msg,delivery_mode=2,
                                        routing_key="sys.circle_new_board",headers={"type":"circle.newreply"},
                                        compression='gzip')
    return Res({"post":newreply.toJson()})
