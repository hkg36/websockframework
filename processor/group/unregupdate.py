#coding:utf-8
from sqlalchemy import and_
from datamodel.group import GroupWatchUpdate
from tools.helper import Res
from tools.session import CheckSession

__author__ = 'amen'
import BackEndEnvData
import dbconfig
@CheckSession
def run(gid):
    with dbconfig.Session() as session:
        session.query(GroupWatchUpdate).filter(and_(GroupWatchUpdate.gid==gid,GroupWatchUpdate.uid==BackEndEnvData.uid)).delete()
        session.commit()
    return Res()