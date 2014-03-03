#coding:utf-8
from datamodel.group import Group
from datamodel.group_member import GroupMember
from tools.helper import Res, CombineGeo
from tools.session import CheckSession

__author__ = 'amen'
import BackEndEnvData
import dbconfig
@CheckSession()
def run(name,board,type=0,position=None,lat=None,long=None):
    with dbconfig.Session() as session:
        newgroup=Group()
        newgroup.creator=BackEndEnvData.uid
        newgroup.group_name=name
        newgroup.group_board=board
        newgroup.type=type
        newgroup.group_postion=position
        if lat and long:
            newgroup.lat=lat
            newgroup.long=long
            newgroup.geokey=CombineGeo(long=long,lat=lat)
        newgroup=session.merge(newgroup)
        session.commit()
        gmember=GroupMember()
        gmember.gid=newgroup.gid
        gmember.uid=BackEndEnvData.uid
        gmember.type=0
        session.merge(gmember)
        session.commit()
        return Res({'gid':newgroup.gid})