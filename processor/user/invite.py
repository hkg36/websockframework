#coding:utf-8
from datamodel.user import UserInviteLog, User
from datamodel.user_circle import CircleDef
from tools.helper import Res, DefJsonEncoder
from tools.session import CheckSession
import BackEndEnvData
import dbconfig
import datetime


@CheckSession()
def run(phone,nick,headpic=None,sex=None,birthday = None,marriage = 0,height = 0,position = None,join_cid=None,join_roleid=None):
    with dbconfig.Session() as session:
        user=session.query(User).filter(User.phone==phone).first()
        if user is not None:
            return Res({'user':user.toJson()},errno=2002,error=u"手机号对应的用户已存在")
    uinl=UserInviteLog.objects(uid=BackEndEnvData.uid,phone=phone).first()
    if uinl is None:
        uinl=UserInviteLog()
        uinl.uid=BackEndEnvData.uid
    uinl.nick=nick
    uinl.phone=phone
    if headpic:
        uinl.headpic=headpic
    if sex:
        uinl.sex=sex
    if birthday:
        uinl.birthday=birthday
    if marriage:
        uinl.marriage=marriage
    if height:
        uinl.height=height
    if position:
        uinl.position=position
    if join_cid:
        uinl.join_cid=join_cid
        with dbconfig.Session() as session:
            cdef=session.query(CircleDef).filter(CircleDef.cid==join_cid).first()
        uinl.join_roleid= cdef.default_roleid

    if (uinl.sms_send_time is None or (datetime.datetime.now()-uinl.sms_send_time).days>1):
        uinl.sms_send_time=datetime.datetime.now()

        userself=session.query(User).filter(User.uid==BackEndEnvData.uid).first()
        json_msg=DefJsonEncoder.encode({'phone':str(phone),
                                        "content":u"手机号%s(%s)的用户邀请你一起玩『来信』,点这里下载 http://t.cn/RvYAd47 "%(userself.phone,userself.nick)})
        BackEndEnvData.queue_producer.publish(body=json_msg,delivery_mode=2,
                                          exchange='sys.sms',routing_key='sms.code',compression='gzip')
    uinl.save()
    return Res({})