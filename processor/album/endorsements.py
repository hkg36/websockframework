from sqlalchemy import and_
from datamodel.Endorsement import EndorsementInfo
from datamodel.user import UserExMedia
import dbconfig
from tools.helper import Res

__author__ = 'amen'

def run(pos=None,count=20):
    with dbconfig.ReadSession() as session:
        usids=session.query(EndorsementInfo.uid).filter(EndorsementInfo.endorsement_type>0).subquery()

        ft=UserExMedia.uid.in_(usids)
        if pos:
            ft=and_(ft,UserExMedia.did<pos)

        medias=[]
        for one in session.query(UserExMedia).filter(ft).order_by(UserExMedia.did.desc()).limit(count):
            medias.append(one.toJson())
        return Res({"media":medias})
