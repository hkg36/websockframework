#coding:utf-8
from datamodel.group import Group
from tools.helper import Res, CombineGeo
from tools.session import CheckSession

__author__ = 'amen'
import BackEndEnvData
import dbconfig
@CheckSession()
def run(gid,name=None,board=None,type=0,position=None,everyone_caninvite=None,only_member_speak=None,only_member_watch=None,
        lat=None,long=None,member_control=None):
    with dbconfig.Session() as session:
        ginfo=session.query(Group).filter(Group.gid==gid).first()
        if ginfo is None:
            return Res({},2,"group not exists")
        if ginfo.creator!=BackEndEnvData.uid:
            return Res({},2,'not creator')
        if name:
            ginfo.group_name = name
        if board:
            ginfo.group_board = board
        if type:
            ginfo.type = type
        if position:
            ginfo.group_postion=position
        if everyone_caninvite is not None:
            ginfo.everyone_caninvite=everyone_caninvite
        if only_member_speak is not None:
            ginfo.only_member_speak=only_member_speak
        if only_member_watch is not None:
            ginfo.only_member_watch=only_member_watch
        if lat and long:
            ginfo.lat=lat
            ginfo.long=long
            ginfo.geokey=CombineGeo(long=long,lat=lat)
        if member_control is not None:
            ginfo.member_control=member_control
        session.merge(ginfo)
        session.commit()

        return Res()
