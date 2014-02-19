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
def run(city,sex):
    with dbconfig.Session() as session:
        allru=session.query(RecommendUser).filter(and_(RecommendUser.city==city,RecommendUser.sex==sex)).\
            order_by(RecommendUser.create_time.desc()).all()
        rus=[]
        for ru in allru:
            rus.append(ru.toJson(show_all=(BackEndEnvData.uid==ru.uid or BackEndEnvData.uid==ru.recommend_uid)))
        return Res({"recommends":rus})