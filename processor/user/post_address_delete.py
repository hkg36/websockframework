from sqlalchemy import and_
from datamodel.user import UserPostAddress
from tools.helper import Res
from tools.session import CheckSession

__author__ = 'amen'
import BackEndEnvData
import dbconfig


@CheckSession()
def run(addrid):
    with dbconfig.Session() as session:
        session.query(UserPostAddress).filter(and_(UserPostAddress.addrid==addrid,UserPostAddress.uid==BackEndEnvData.uid)).delete()
        session.commit()
        return Res({})

