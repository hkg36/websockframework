#coding:utf-8
from sqlalchemy import distinct
from datamodel.Endorsement import Endorsement
from datamodel.merchandise import StoreMerchandise
from datamodel.user import User
import dbconfig
from tools.helper import Res

__author__ = 'amen'

def run(uid):
    with dbconfig.Session() as session:
        user_list=[]
        for einof,sm in session.query(Endorsement,StoreMerchandise).join(StoreMerchandise,Endorsement.mid==StoreMerchandise.mid).all():
            user_list.append({"merchandise":sm.toJson2(),"endorsement":einof.toJson()})
        return Res({"users":user_list})