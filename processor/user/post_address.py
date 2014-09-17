from datamodel.user import UserPostAddress
from tools.helper import Res
from tools.session import CheckSession

__author__ = 'amen'
import BackEndEnvData
import dbconfig


@CheckSession()
def run():
    with dbconfig.Session() as session:
        addrs=[]
        for one in session.query(UserPostAddress).filter(UserPostAddress.uid==BackEndEnvData.uid).all():
            addrs.append(one.toJson())
        return Res({'address':addrs})