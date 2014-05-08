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

        users_circle=session.query(UserCircle,CircleDef).join(CircleDef,and_(UserCircle.cid==CircleDef.cid,UserCircle.subid==CircleDef.subid)).filter(UserCircle.uid.in_(uids)).all()
        circles={}
        for uc,cdef in users_circle:
            ll=circles.get(uc.uid,[])
            ll.append({'cid':uc.cid,'subid':uc.subid,'title':cdef.title,'level':cdef.level,'time':uc.time,"by_uid":uc.by_uid})
            circles[uc.uid]=ll

        for u in users:
            udata=u.toJson()
            udata['circle']=circles.get(u.uid,None)
            ulist.append(udata)

        return Res({"users":ulist})