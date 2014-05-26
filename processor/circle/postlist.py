from tools.session import CheckSession

__author__ = 'amen'
from datamodel.user_circle import CircleDef, UserCircle, CircleBoardHistory, CirclePost
from tools.helper import Res
import BackEndEnvData
import dbconfig

@CheckSession()
def run(cid,before_postid=None,count=20):
    params={'cid':cid}
    if before_postid is not None:
        params['postid__lt']=before_postid
    posts=CirclePost.objects(**params).order_by("-postid").limit(count)
    allpost=[]
    for one in posts:
        allpost.append(one.toJson())
    return Res({"posts":allpost})
