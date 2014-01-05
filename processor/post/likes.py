from sqlalchemy import and_
from datamodel.post import Post
from datamodel.post_like import PostLike
from tools.helper import Res
from tools.session import CheckSession

__author__ = 'amen'
import BackEndEnvData
import dbconfig
@CheckSession
def run(postid,pos=0,count=50):
    with dbconfig.Session() as session:
        lks=session.query(PostLike).filter(PostLike.postid==postid).order_by(PostLike.time.desc()).offset(pos).limit(count).all()
        lklist=[]
        for lk in lks:
            lklist.append({'uid':lk.uid,'time':lk.time})
    return Res({'users':lklist})