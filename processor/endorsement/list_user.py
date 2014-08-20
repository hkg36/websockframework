#coding:utf-8
from datamodel.Endorsement import EndorsementInfo
import dbconfig
from tools.helper import Res

__author__ = 'amen'

def run():
    with dbconfig.Session() as session:
        user_list=[]
        for uid,time in session.query(EndorsementInfo.uid,EndorsementInfo.create_time).\
            filter(EndorsementInfo.endorsement_type>0).order_by(EndorsementInfo.order_weigth.desc()).all():
            user_list.append({"uid":uid,"time":time})
        return Res({"users":user_list})