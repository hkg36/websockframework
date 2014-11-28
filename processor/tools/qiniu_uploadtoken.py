#coding:utf-8
from tools.helper import Res
from tools.session import CheckSession
import dbconfig
import qiniu

@CheckSession()
def run():
    uptoken = dbconfig.qiniuAuth.upload_token(dbconfig.qiniuSpace,policy={"returnBody":'{"errno":0,"error":"Success","url":"http://$(bucket).qiniudn.com/$(key)"}'})
    return Res({'token':uptoken})