#coding:utf-8
from mongoengine import *
import datetime

__author__ = 'amen'

class TenpayState(Document):
    orderid=StringField(required=True,primary_key=True)
    mid=LongField(required=True)
    desc=StringField(required=True)
    uid=LongField(required=True)
    paystate=IntField(default=0)
    create_time=DateTimeField(default=datetime.datetime.now)
    paytime=DateTimeField()
    refundtime=DateTimeField()
    transaction_id=StringField()
    remain=IntField(default=0)
    ex_people=IntField()
    recm_uid=LongField(default=0)

    meta = {
        'indexes': [('uid','-orderid'),'recm_uid']
    }

    def toJson(self):
        data={'orderid':self.orderid,
              'mid':self.mid,
              "desc":self.desc,
              'uid':self.uid,
              'paystate':self.paystate,
              'create_time':self.create_time,
              'paytime':self.paytime,
              'refundtime':self.refundtime,
              'remain':self.remain,
              'ex_people':self.ex_people,
              'recommend_uid':self.recm_uid}
        return data

class TenpayLog(Document):
    payid=SequenceField(primary_key=True)
    orderid=StringField(required=True)
    mid=LongField(required=True)
    uid=LongField(required=True)
    paystate=IntField(required=True)
    desc=StringField(required=True)
    amount=IntField(required=True)
    ex_people=IntField()
    create_time=DateTimeField(default=datetime.datetime.now)
    recm_uid=LongField()

    pay_info=StringField()
    bank_type=StringField()
    bank_billno=StringField()
    time_end=StringField()
    purchase_alias=StringField()

    def __init__(self,paystate):
        super(TenpayLog,self).__init__()
        self.orderid=paystate.orderid
        self.mid=paystate.mid
        self.uid=paystate.uid
        self.paystate=paystate.paystate
        self.desc=paystate.desc
        self.amount=paystate.remain
        self.ex_people=paystate.ex_people
        self.recm_uid=paystate.recm_uid
    def toJson(self):
        data={
            'payid':self.payid,
            'orderid':self.orderid,
            'mid':self.mid,
            'uid':self.uid,
            'paystate':self.paystate,
            'desc':self.desc,
            'amount':self.amount,
            'create_time':self.create_time,
            'ex_people':self.ex_people,
            'recommend_uid':self.recm_uid
        }
        return data