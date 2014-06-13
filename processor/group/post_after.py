from datamodel.post2 import GroupPost
from tools.session import CheckSession

__author__ = 'amen'
from tools.helper import Res
import BackEndEnvData
import dbconfig

@CheckSession()
def run(gid,after_postid):
    params={'gid':gid}
    params['postid__gt']=after_postid
    posts=GroupPost.objects(**params).order_by("-postid").limit(100)
    allpost=[]
    for one in posts:
        allpost.append(one.toJson())
    return Res({"posts":allpost})
