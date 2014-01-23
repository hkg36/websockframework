#coding:utf-8
from datamodel.group_member import GroupMember
from tools.helper import Res
from tools.session import CheckSession

__author__ = 'amen'
import BackEndEnvData
import dbconfig
import json
@CheckSession()
def run(gid,type=1):
    with dbconfig.Session() as session:
        gmember=GroupMember()
        gmember.gid=gid
        gmember.uid=BackEndEnvData.uid
        gmember.type=type
        session.merge(gmember)
        session.commit()
    return Res()
