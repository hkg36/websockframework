from datamodel.user import UserExData, UserLikeLog
from tools.helper import Res
from tools.session import CheckSession

__author__ = 'amen'
import BackEndEnvData
import dbconfig


@CheckSession()
def run(uid):
    if uid==BackEndEnvData.uid:
        return Res(errno=2,error="like self")
    with dbconfig.Session() as session:
        new_like=UserLikeLog()
        new_like.uid=uid
        new_like.by_uid=BackEndEnvData.uid
        session.add(new_like)
        try:
            session.commit()
        except Exception,e:
            return Res(errno=2,error="has liked")
    UserExData.objects(uid=uid).update_one(upsert=True, inc__like_me_count=1)
    return Res()