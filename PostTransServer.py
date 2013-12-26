import QueueWorker2
import getopt
import importlib
import sys
from datamodel.connection_info import ConnectionInfo
from datamodel.group import GroupWatchUpdate
from datamodel.friendlist import FriendList
import dbconfig
import anyjson
import zlib


class PostTransServer(QueueWorker2.QueueWorker):
    def RequestWork(self,params,body,reply_queue):
        post=anyjson.loads(body)
        gid=post['gid']
        uid=post['uid']
        uids=set()
        session=dbconfig.Session()
        gwus=session.query(GroupWatchUpdate).filter(GroupWatchUpdate.gid==gid).all()
        for gwu in gwus:
            uids.add(gwu.uid)
        fds=session.query(FriendList).filter(FriendList.friendid==uid).all()
        for fd in fds:
            uids.add(fd.uid)
        allconn=session.query(ConnectionInfo).filter(ConnectionInfo.uid.in_(list(uids))).all()
        session.close()
        to_push=anyjson.dumps({"push":True,
                                    "type":"newpost",
                                    "data":{
                                        "post":post
                                    }
                                })
        for conn in allconn:
            self.producer.publish(body=to_push,delivery_mode=2,headers={"connid":conn.connection_id},
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
    worker=PostTransServer(configs.Queue_Server,configs.Queue_Port,configs.Queue_Path,
                    configs.Queue_User,configs.Queue_PassWord,'sys.post_to_notify')
    worker.run()