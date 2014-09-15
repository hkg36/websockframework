#coding:utf-8
from datamodel.Endorsement import EndorsementTimes
import dbconfig
import BackEndEnvData
from tools.helper import Res
from tools.session import CheckSession


@CheckSession()
def run():
    with dbconfig.Session() as session:
        etlist=session.query(EndorsementTimes).filter(EndorsementTimes.uid==BackEndEnvData.uid).all()
        ets=[]
        for one in etlist:
            ets.append((one.start_date,one.stop_date))
        return Res({"times":ets})