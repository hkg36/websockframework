from datamodel.user import User
from paylib.SmsWap import MerchantAPI
from tools.helper import Res
from tools.session import CheckSession

__author__ = 'amen'
import BackEndEnvData
import dbconfig
@CheckSession()
def run():
    with dbconfig.Session() as session:
        usr=session.query(User).filter(User.uid==BackEndEnvData.uid).first()
        mer=MerchantAPI()
        try:
            cardlist=mer.BindList(usr.phone,4)
        except Exception,e:
            return Res({'cards':[]})
        cards=[]
        for c in cardlist:
            cards.append({'card_name':c['card_name'],
                          'cardid':c['bindid'],
                          'card_last':c['card_last'],
                          'card_top':c['card_top'],
                          'bindvalidthru':c['bindvalidthru']})
        return Res({'cards':cards})
