#coding:utf-8
from datamodel.post2 import GroupPost
from tools.helper import Res
from tools.session import CheckSession


__author__ = 'amen'
import BackEndEnvData
import dbconfig

@CheckSession()
def run(gid,before_postid=None,count=20):
    query=dict(gid=gid)
    if before_postid:
        query['postid__lt']=before_postid
    posts=[]
    for one in GroupPost.objects(**query).order_by("-postid").limit(count):
        posts.append(one.toJson())
    return Res({"posts":posts})