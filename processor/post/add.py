from datamodel.post import Post
from tools.addPushQueue import AddPostPublish
from tools.helper import Res
from tools.session import CheckSession

__author__ = 'amen'
import BackEndEnvData
import dbconfig

@CheckSession
def run(gid,content):
    session=dbconfig.Session()
    newpost=Post()
    newpost.uid=BackEndEnvData.uid
    newpost.group_id=gid
    newpost.content=content
    newpost=session.merge(newpost)
    session.flush()
    newpost_id=newpost.postid
    newpost_json=newpost.toJson()
    session.commit()
    session.close()
    AddPostPublish(newpost_json)
    return Res({'postid':newpost_id})