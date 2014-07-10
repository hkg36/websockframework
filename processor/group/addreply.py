from datamodel.post2 import GroupPost
from tools.session import CheckSession, FrequencyControl

__author__ = 'amen'
from datamodel.user_circle import ReplyRecord
from tools.helper import Res, DefJsonEncoder
import BackEndEnvData
import dbconfig

@CheckSession()
@FrequencyControl()
def run(postid,content):
    newpost=GroupPost.objects(postid=postid).first()
    newreply=ReplyRecord()
    newreply.uid=BackEndEnvData.uid
    newreply.content=content
    newpost.replys.append(newreply)
    newpost.save()

    json_msg=DefJsonEncoder.encode({'reply':newreply.toJson(),"gid":newpost.gid,'postid':newpost.postid})
    BackEndEnvData.queue_producer.publish(body=json_msg,delivery_mode=2,
                                        routing_key="group.change",headers={"type":"group.newreply"},
                                        compression='gzip')

    return Res({"post":newreply.toJson()})