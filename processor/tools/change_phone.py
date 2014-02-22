#coding:utf-8
import random
from datamodel.user import User
from tools.helper import Res
from tools.session import CheckSession
import dbconfig
import BackEndEnvData
import tools.addPushQueue

@CheckSession()
def run(newphone,code=None):
    if code is None:
        with dbconfig.Session() as session:
            user=session.query(User).filter(User.uid==BackEndEnvData.uid).first()
            if user.phone == newphone:
                return Res(errno=1001,error="phone is the same")
            user=session.query(User).filter(User.phone==newphone).first()
            if user is not None:
                return Res(errno=1002,error="phone use by other accout")
            gcode=str(random.randint(1000,9999))
            dbconfig.memclient.set("changephone:%d"%BackEndEnvData.uid,{"phone":newphone,"code":gcode},time=60*60)
            tools.addPushQueue.AddSMS(newphone,gcode)
            return Res({"code":gcode})
    else:
        with dbconfig.Session() as session:
            user=session.query(User).filter(User.uid==BackEndEnvData.uid).first()
            data=dbconfig.memclient.get("changephone:%d"%BackEndEnvData.uid)
            if data is None:
                return Res(errno=3,error="not verfy code has send")
            if data['code']!=code:
                return Res(errno=1003,error="verfy code error")
            dbconfig.memclient.delete("changephone:%d"%BackEndEnvData.uid)
            user.phone=data["phone"]
            session.merge(user)
            session.commit()
            return Res({'newphone':data["phone"]})