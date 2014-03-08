from sqlalchemy import and_
from datamodel.user import UserExMedia
from tools.helper import Res
from tools.session import CheckSession

__author__ = 'amen'
import BackEndEnvData
import dbconfig

@CheckSession()
def run(did):
    with dbconfig.Session() as session:
        row_count=session.query(UserExMedia).filter(and_(UserExMedia.uid==BackEndEnvData.uid,UserExMedia.did==did)).delete('fetch')
        session.commit()
        if row_count>0:
            return Res()
        else:
            return Res(errno=2,error='not exists or not yours')