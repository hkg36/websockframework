from sqlalchemy import and_
from datamodel.user import User
from datamodel.user_circle import UserCircle, CircleDef
from tools.helper import Res
from tools.session import CheckSession

__author__ = 'amen'
import BackEndEnvData
import dbconfig

SEARCH_R=0.03
@CheckSession()
def run(phone):
    with dbconfig.Session() as session:
        users=session.query(User).join(UserCircle,UserCircle.uid==User.uid).filter(and_(User.phone.like(phone+"%"),UserCircle.cid!=None)).limit(4).all()
        ulist=[]
        uids=[u.uid for u in users]

        for u in users:
            udata=u.toJson()
            ulist.append(udata)

        return Res({"users":ulist})