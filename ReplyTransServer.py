import QueueWork
import getopt
import importlib
import sys
from datamodel.connection_info import ConnectionInfo
from datamodel.group import GroupWatchUpdate
from datamodel.friendlist import FriendList
from datamodel.group_member import GroupMember
from datamodel.post import Post
import dbconfig
import json
import zlib

def RequestWork(params,body,reply_queue):
    reply=json.loads(body)
    postid=reply['postid']
    with dbconfig.Session() as session:
        post=session.query(Post).filter(Post.postid==postid).first()
        if post.uid==reply['uid']:
            return
        conn=session.query(ConnectionInfo).filter(ConnectionInfo.uid==post.uid).first()
        to_push=json.dumps({"push":True,
                                "type":"newreply",
                                "data":{
                                    "reply":reply
                                }
                            })
        QueueWork.producer.publish(body=to_push,delivery_mode=2,headers={"connid":conn.connection_id},
                                  routing_key=conn.queue_id,
                                  compression='gzip')
if __name__ == '__main__':
    config_model='configs.frontend'
    opts, args=getopt.getopt(sys.argv[1:],'c:',
                             ['config='])
    for k,v in opts:
        if k in ('-c','--config'):
            config_model=v
    try:
        configs=importlib.import_module(config_model)
    except Exception,e:
        print str(e)
        exit(0)
    QueueWork.WorkFunction=RequestWork
    QueueWork.init(configs.Queue_Server,configs.Queue_Port,configs.Queue_Path,
                    configs.Queue_User,configs.Queue_PassWord,'sys.newreply')
    QueueWork.run()
