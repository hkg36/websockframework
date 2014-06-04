#coding:utf-8
from tools.helper import Res
from tools.session import CheckSession
import dbconfig
import qiniu
import qiniu.rs

@CheckSession()
def run():
    policy = qiniu.rs.PutPolicy(dbconfig.qiniuSpace)
    policy.returnBody='{"errno":0,"error":"Success","url":"http://$(bucket).qiniudn.com/$(key)"}'
    uptoken =policy.token()
    return Res({'token':uptoken})