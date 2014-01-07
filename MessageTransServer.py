__author__ = 'amen'
import QueueWork
import getopt
import importlib
import sys
from datamodel.connection_info import ConnectionInfo
from datamodel.group import GroupWatchUpdate
from datamodel.friendlist import FriendList
import dbconfig
import anyjson
import zlib

def RequestWork(self,params,body,reply_queue):
    post=anyjson.loads(body)
    toid=post['toid']
    with dbconfig.Session() as session:
        conn=session.query(ConnectionInfo).filter(ConnectionInfo.uid==toid).first()
    to_push=anyjson.dumps({"push":True,
                                "type":"newmsg",
                                "data":{
                                    "message":post
                                }
                            })
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
    QueueWork.WorkFunction=RequestWork
    QueueWork.init(configs.Queue_Server,configs.Queue_Port,configs.Queue_Path,
                    configs.Queue_User,configs.Queue_PassWord,'sys.message_to_notify')
    QueueWork.run()