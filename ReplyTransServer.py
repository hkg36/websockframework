#coding:utf-8
import getopt
import importlib
import sys
import json

import QueueWork
from datamodel.connection_info import ConnectionInfo
from datamodel.post import Post
from datamodel.post_like import PostLike
from datamodel.post_reply import PostReply
import dbconfig
from tools.helper import AutoFitJson


def RequestWork(params,body,reply_queue):
    reply=json.loads(body)
    postid=reply['postid']
    with dbconfig.Session() as session:
        to_uid=set()
        likes=session.query(PostLike).filter(PostLike.postid==postid).all()
        for a in likes:
            to_uid.add(a.uid)
        replys=session.query(PostReply).filter(PostReply.postid==postid).order_by(PostReply.replyid.desc()).limit(50).all()
        for a in replys:
            to_uid.add(a.uid)
        post=session.query(Post).filter(Post.postid==postid).first()
        to_uid.add(post.uid)
        if reply['uid'] in to_uid:
            to_uid.remove(reply['uid'])

        conns=session.query(ConnectionInfo).filter(ConnectionInfo.uid.in_(list(to_uid))).all()
        to_push=json.dumps({"push":True,
                                "type":"newreply",
                                "data":{
                                    "gid":post.group_id,
                                    "reply":reply
                                }
                            },ensure_ascii=False,cls=AutoFitJson,separators=(',', ':'))
        for conn in conns:
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
