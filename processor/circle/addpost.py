from tools.session import CheckSession

__author__ = 'amen'
from datamodel.user_circle import CircleDef, UserCircle, CircleBoardHistory, CirclePost
from tools.helper import Res
import BackEndEnvData
import dbconfig

@CheckSession()
def run(cid,content,pictures=[]):
    if isinstance(pictures,list)==False:
        pictures=[pictures]
    newpost=CirclePost()
    newpost.picture_list=pictures
    newpost.cid=cid
    newpost.uid=BackEndEnvData.uid
    newpost.content=content
    newpost.save()
    return Res({"post":newpost.toJson()})
