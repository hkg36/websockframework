from sqlalchemy import and_
from datamodel.Recommend import RecommendUser
from datamodel.user import User
from tools.helper import Res
from tools.session import CheckSession

__author__ = 'amen'
import BackEndEnvData
import dbconfig
@CheckSession()
def run(uid,recommend_id,recommend_word=None,city=None,sex=None,sex_want=None,contact=None,age=None,tags=None):
    if uid!=BackEndEnvData.uid and recommend_id!=BackEndEnvData.uid:
        return Res(errno=2,error="can not modify")
    with dbconfig.Session() as session:
        ru=session.query(RecommendUser).filter(and_(RecommendUser.uid==uid,RecommendUser.recommend_uid==recommend_id)).first()
        if recommend_word:
            ru.recommend_word=recommend_word
        if city:
            ru.city=city
        if sex:
            ru.sex=sex
        if sex_want:
            ru.sex_want=sex_want
        if contact:
            ru.contact=contact
        if age:
            ru.age=age
        if tags and isinstance(tags,list):
            ru.tags='|'.join(tags)
        session.merge(ru)
        session.commit()
    return Res()