from datamodel.user import User
from tools.helper import Res
from tools.session import CheckSession

__author__ = 'amen'
import BackEndEnvData
import dbconfig
import anyjson
@CheckSession
def run(nick, sex, birthday, marriage, height):
    session=dbconfig.Session()
    user=session.query(User).filter(User.uid==BackEndEnvData.uid).first();
    if user is None:
        return Res(errno=3,error='data error')
    user.nick=nick
    user.sex=sex
    user.birthday=birthday
    user.marriage=marriage
    user.height=height
    session.merge(user)
    session.commit()
    return Res()