#coding:utf-8
import time
from kombu import Exchange, Producer
from sqlalchemy import and_, or_

from datamodel.ios import IOSDevice
from datamodel.merchandise import StoreWeixinNotify
from datamodel.user import User
from tools.helper import AutoFitJson


__author__ = 'amen'
import QueueWork
import getopt
import importlib
import sys
from datamodel.connection_info import ConnectionInfo
import dbconfig
import json
import tools.weixin as weixin

def RequestWork(params,body,reply_queue):
    post=json.loads(body)
    to_weixin_user=set(post.get('weixin_users',[]))
    if len(to_weixin_user)==0:
        return
    msgbody={
        "msgtype":"text",
        "text":
        {
             "content":post['content']
        }
    }
    token=weixin.GetAccessToken()
    for u in to_weixin_user:
        msgbody["touser"]=u
        data=weixin.SendMessage(token,msgbody)
exchange=None
publish_debug_exchange = None
publish_release_exchange = None
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
                    configs.Queue_User,configs.Queue_PassWord,'sys.sendweixin')
    QueueWork.run()
