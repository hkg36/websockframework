#coding:utf-8
from datamodel.Endorsement import EndorsementTimes
import dbconfig
import BackEndEnvData
from tools.helper import Res
from tools.session import CheckSession
import datetime


@CheckSession()
def run(times):
    with dbconfig.Session() as session:
        session.query(EndorsementTimes).filter(EndorsementTimes.uid==BackEndEnvData.uid).delete()
        for one in times:
            et=EndorsementTimes()
            et.uid=BackEndEnvData.uid
            et.start_date=datetime.datetime.fromtimestamp(one[0])
            et.stop_date=datetime.datetime.fromtimestamp(one[1])
            session.merge(et)
        session.commit()
        return Res()
