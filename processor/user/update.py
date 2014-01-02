from datamodel.user import User
from tools.helper import Res
from tools.session import CheckSession

__author__ = 'amen'
import BackEndEnvData
import dbconfig
import anyjson
@CheckSession
def run(nick=None,signature=None, sex=None, birthday=None, marriage=None, height=None):
    session=dbconfig.Session()
    user=session.query(User).filter(User.uid==BackEndEnvData.uid).first();
    if user is None:
        return Res(errno=3,error='data error')
    if nick:
        user.nick=nick
    if signature:
        user.signature=signature
    if sex:
        user.sex=sex
    if birthday:
        user.birthday=birthday
    if marriage:
        user.marriage=marriage
    if height:
        user.height=height

    session.merge(user)
    session.commit()
    session.close()
    return Res()