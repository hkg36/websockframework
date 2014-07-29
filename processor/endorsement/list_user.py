#coding:utf-8
from sqlalchemy import distinct
from datamodel.Endorsement import EndorsementInfo
from datamodel.user import User
import dbconfig
from tools.helper import Res

__author__ = 'amen'

def run():
    with dbconfig.Session() as session:
        user_list=[]
        for einof,user in session.query(EndorsementInfo,User).join(User,EndorsementInfo.uid==User.uid).\
            filter(EndorsementInfo.endorsement_type>0).all():
            user_list.append({"user":user.toJson(),"endorsement":einof.toJson()})
        return Res({"users":user_list})