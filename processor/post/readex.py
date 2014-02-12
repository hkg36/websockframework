#coding:utf-8
from datamodel.post import PostExData
from tools.helper import Res
from tools.session import CheckSession
import dbconfig
@CheckSession()
def run(postid):
    with dbconfig.Session() as session:
        exdatas=session.query(PostExData).filter(PostExData.postid==postid).all()
        exlist=[]
        for e in exdatas:
            exlist.append(e.toJson())
        return Res({'exdata':exlist})