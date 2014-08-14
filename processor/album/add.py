#coding:utf-8
import BackEndEnvData
from datamodel.user import UserExMedia
import dbconfig
from tools.helper import Res
from tools.session import CheckSession

@CheckSession()
def run(url,filetype,content=None,width=None,height=None,length=None):
    with  dbconfig.Session() as session:
        exmedia=UserExMedia()
        exmedia.uid=BackEndEnvData.uid
        exmedia.text=content
        fileurl=url
        if filetype==1:
            exmedia.picture=fileurl
            exmedia.width=width
            exmedia.height=height
        elif filetype==2:
            exmedia.voice=fileurl
            exmedia.length=length
        elif filetype==3:
            exmedia.video=fileurl
            exmedia.length=length
        exmedia=session.merge(exmedia)
        session.commit()
        return Res({'did':exmedia.did})