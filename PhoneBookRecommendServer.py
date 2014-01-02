from sqlalchemy import not_, and_

__author__ = 'amen'
import QueueWorker2
import getopt
import importlib
import sys
from datamodel.connection_info import ConnectionInfo
from datamodel.group import GroupWatchUpdate
from datamodel.friendlist import FriendList
from datamodel.phone_book import PhoneBook
from datamodel.user import User
import dbconfig
import anyjson
import zlib


class PhoneBookRecommendServer(QueueWorker2.QueueWorker):
    def RequestWork(self,params,body,reply_queue):
        post=anyjson.loads(body)
        uid=post['uid']
        session=dbconfig.Session()
        phonelist=session.query(PhoneBook).filter(PhoneBook.uid==uid).all()
        phones=[]
        for pinfo in phonelist:
            phones.append(pinfo.phone)
        fds=session.query(FriendList).filter(FriendList.uid==uid).all()
        friendids=[]
        for fd in fds:
            friendids.append(fd.friendid)

        if friendids:
            users=session.query(User).filter(and_(User.phone.in_(phones),not_(User.uid.in_(friendids)))).all()
        else:
            users=session.query(User).filter(User.phone.in_(phones)).all()
        userlist=[]
        for u in users:
            userlist.append(u.toJson(showphone=True))
        conn=session.query(ConnectionInfo).filter(ConnectionInfo.uid==uid).first()
        session.close()
        to_push=anyjson.dumps({"push":True,
                                    "type":"fromphonebook",
                                    "data":{
                                        "users":userlist
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
    worker=PhoneBookRecommendServer(configs.Queue_Server,configs.Queue_Port,configs.Queue_Path,
                    configs.Queue_User,configs.Queue_PassWord,'sys.user_phonebook_update')
    worker.run()