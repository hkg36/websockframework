from tools.session import CheckSession

__author__ = 'amen'
from datamodel.user_circle import CircleDef, UserCircle, CircleBoardHistory, CirclePost
from tools.helper import Res, DefJsonEncoder
import BackEndEnvData
import dbconfig

@CheckSession()
def run(cid,content,pictures=[],mid=None):
    if isinstance(pictures,list)==False:
        pictures=[pictures]
    newpost=CirclePost()
    newpost.picture_list=pictures
    newpost.cid=cid
    newpost.uid=BackEndEnvData.uid
    newpost.content=content
    newpost.mid=mid
    newpost.save()
    json_msg=DefJsonEncoder.encode(newpost.toJson())
    BackEndEnvData.queue_producer.publish(body=json_msg,delivery_mode=2,
                                        routing_key="sys.circle_new_board",headers={"type":"circle.newpost"},
                                        compression='gzip')
    return Res({"postid":newpost.postid})
