from datamodel.user import User
from tools.helper import Res
from tools.session import CheckSession

__author__ = 'amen'
import BackEndEnvData
import dbconfig

SEARCH_R=0.03
@CheckSession()
def run(phone):
    with dbconfig.Session() as session:
        users=session.query(User).filter(User.phone.like(phone+"%")).limit(4).all()
        ulist=[]
        for u in users:
            ulist.append(u.toJson())
        return Res({"users":ulist})