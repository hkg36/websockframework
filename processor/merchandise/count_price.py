import random
import time
from datamodel.merchandise import StoreMerchandise, StorePayState
from datamodel.user import User
from paylib.SmsWap import MerchantAPI
from tools.helper import Res
from tools.session import CheckSession

__author__ = 'amen'
import BackEndEnvData
import dbconfig

def get_price(sm,**kwargs):
    people_count=kwargs.get('people_count',None)
    return sm.amount+sm.ex_people_amount*people_count
def run(mid,people_count):
    with dbconfig.Session() as session:
        sm=session.query(StoreMerchandise).filter(StoreMerchandise.mid==mid).first()
        if sm is None:
            return Res(errno=2,error="mid not exists")
        price=get_price(sm,people_count=people_count)
        return Res({'price':price})