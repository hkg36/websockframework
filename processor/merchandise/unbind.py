from datamodel.user import User
from paylib.SmsWap import MerchantAPI
from tools.helper import Res
from tools.session import CheckSession

__author__ = 'amen'
import BackEndEnvData
import dbconfig
@CheckSession()
def run(cardid):
    with dbconfig.Session() as session:
        usr=session.query(User).filter(User.uid==BackEndEnvData.uid).first()
        mer=MerchantAPI()
        result=mer.UnbindCardsign(cardid,usr.phone,4)
        if 'error_code' in result:
            return Res(result,errno=3,error='fail')
        else:
            return Res({'cardid':result.get('bindid')})