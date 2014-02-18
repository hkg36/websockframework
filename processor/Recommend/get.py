from sqlalchemy import and_
from datamodel.Recommend import RecommendUser
from tools.helper import Res
from tools.session import CheckSession

__author__ = 'amen'
import BackEndEnvData
import dbconfig
@CheckSession()
def run(uid,recommend_uid):
    with dbconfig.Session() as session:
        ru=session.query(RecommendUser).filter(and_(RecommendUser.uid==uid,RecommendUser.recommend_uid==recommend_uid)).first()
        return Res({"info":ru.toJson(ru.uid==BackEndEnvData.uid or ru.recommend_uid==BackEndEnvData.uid)})