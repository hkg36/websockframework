#coding:utf-8
from datamodel.group_member import GroupMember
from tools.helper import Res
from tools.session import CheckSession

__author__ = 'amen'
import BackEndEnvData
import dbconfig
@CheckSession()
def run(gid):
    with dbconfig.Session() as session:
        members=session.query(GroupMember).filter(GroupMember.gid==gid).order_by(GroupMember.time.desc()).all()
        memberlist=[]
        for m in members:
            memberlist.append({'uid':m.uid,"type":m.type,"time":m.time})
        return Res({'members':memberlist})