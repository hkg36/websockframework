#coding:utf-8
from sqlalchemy import and_
from datamodel.Recommend import RecommendMedia
from tools.helper import Res
from tools.session import CheckSession
import dbconfig
@CheckSession()
def run(uid,recommend_uid):
    with dbconfig.Session() as session:
        medias=session.query(RecommendMedia).filter(and_(RecommendMedia.uid==uid,RecommendMedia.recommend_uid==recommend_uid)).all()
        mediaslist=[]
        for e in medias:
            mediaslist.append(e.toJson())
        return Res({'exdata':mediaslist})