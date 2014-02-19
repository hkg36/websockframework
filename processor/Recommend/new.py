from datamodel.Recommend import RecommendUser
from datamodel.events import Events
from datamodel.user import User
from tools.addPushQueue import AddEventNotify
from tools.helper import Res
from tools.session import CheckSession

__author__ = 'amen'
import BackEndEnvData
import dbconfig
@CheckSession()
def run(uid,recommend_word,city,sex,sex_want,contact,age,tags):
    with dbconfig.Session() as session:
        user=session.query(User).filter(User.uid==uid)
        if user is None:
            return Res({},errno=3,error='user not exists')
        ru=RecommendUser()
        ru.uid=uid
        ru.recommend_uid=BackEndEnvData.uid
        ru.recommend_word=recommend_word
        ru.city=city
        ru.sex=sex
        ru.sex_want=sex_want
        ru.contact=contact
        ru.age=age
        if isinstance(tags,list):
            ru.tags='|'.join(tags)

        session.merge(ru)
        session.commit()

        event=Events()
        event.touid=uid
        event.param1=uid
        event.param2=BackEndEnvData.uid
        event.type="recommend"
        event=session.merge(event)
        session.commit()

        AddEventNotify(event)

    return Res()