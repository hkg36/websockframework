from tools.session import CheckSession

__author__ = 'amen'
from datamodel.user_circle import CirclePost
from tools.helper import Res
import BackEndEnvData
import dbconfig

@CheckSession()
def run(cid,after_postid):
    params={'cid':cid}
    params['postid__gt']=after_postid
    posts=CirclePost.objects(**params).order_by("-postid").limit(100)
    allpost=[]
    for one in posts:
        allpost.append(one.toJson())
    return Res({"posts":allpost})
