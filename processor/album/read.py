from sqlalchemy import and_
from datamodel.user import UserExMedia
from tools.helper import Res
from tools.session import CheckSession

__author__ = 'amen'
import BackEndEnvData
import dbconfig

@CheckSession()
def run(uid,before=None,count=10):
    with dbconfig.Session() as session:
        query=session.query(UserExMedia)
        if before is None:
            query=query.filter(UserExMedia.uid==uid)
        else:
            query=query.filter(and_(UserExMedia.uid==uid,UserExMedia.did<before))
        query=query.order_by(UserExMedia.did.desc()).limit(count)

        medias=query.all()
        medialist=[]
        for media in medias:
            medialist.append(media.toJson())
        return Res({'medias':medialist})