from sqlalchemy import and_
from datamodel.Recommend import RecommendUser
from datamodel.friendlist import FriendList
from datamodel.user import User
from tools.helper import Res
from tools.session import CheckSession

__author__ = 'amen'
import BackEndEnvData
import dbconfig
@CheckSession()
def run():
    with dbconfig.Session() as session:
        friendlist=session.query(FriendList).filter(FriendList.uid==BackEndEnvData.uid).all()
        friendids=[]
        for f in friendlist:
            friendids.append(f.friendid)

        allru=session.query(RecommendUser).filter(RecommendUser.recommend_uid.in_(friendids)).order_by(RecommendUser.create_time.desc()).all()
        allrulist=[]
        for ru in allru:
            allrulist.append(ru.toJson(show_all=(BackEndEnvData.uid==ru.uid or BackEndEnvData.uid==ru.recommend_uid)))
        return Res({"recommends":allrulist})