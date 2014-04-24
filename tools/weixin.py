import urllib2
import json
from poster.encode import multipart_encode
from poster.streaminghttp import register_openers
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
import time
import pycurl
from cStringIO import StringIO
from dbconfig import AutoSession

register_openers()

apps={'wx2cffd0c7bb254e6a':'7347dd97348c1cad2e9e5d409145fcf8'}

DBBase=declarative_base(name="WinxinBase")
db=create_engine("sqlite:///data/weixinbase.sqlite")
class WeixinAccessToken(DBBase):
    __tablename__ = 'weixin_access_token'
    appid=Column(String(32),primary_key=True,nullable=False)
    access_token=Column(String(256),nullable=False)
    time=Column(Integer,nullable=False)
DBBase.metadata.create_all(db)
Session = sessionmaker(bind=db,autocommit=False,autoflush=False,class_=AutoSession)

def GetAccessToken():
    return get_weixin_token('wx2cffd0c7bb254e6a')
def get_weixin_token(appid):
    if appid not in apps:
        raise Exception('appid is error')
    appsecret=apps[appid]
    with Session() as session:
        weixin_token=session.query(WeixinAccessToken).filter(and_(WeixinAccessToken.appid==appid,WeixinAccessToken.time>time.time())).first()
        if weixin_token:
            return weixin_token.access_token
        resbody=urllib2.urlopen('https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s'%(appid,appsecret)).read()
        data=json.loads(resbody)
        weixin_token=WeixinAccessToken()
        weixin_token.appid=appid
        weixin_token.access_token=data['access_token']
        weixin_token.time=time.time()+data['expires_in']-200
        session.merge(weixin_token)
        session.commit()
        return weixin_token.access_token
def PostFile(token,file,type='image'):
    datagen, headers = multipart_encode({"media": open(file, "rb")})
    request = urllib2.Request("http://file.api.weixin.qq.com/cgi-bin/media/upload?access_token=%s&type=%s"%(token,type), datagen, headers)
    data=json.loads(urllib2.urlopen(request).read())
    return data['media_id']
def GetFile(token,media_id):
    request = urllib2.Request("http://file.api.weixin.qq.com/cgi-bin/media/get?access_token=%s&media_id=%s"%(token,media_id))
    data=urllib2.urlopen(request).read()
    return data
def SendMessage(token,json_message):
    """
    http://mp.weixin.qq.com/wiki/index.php?title=%E5%8F%91%E9%80%81%E5%AE%A2%E6%9C%8D%E6%B6%88%E6%81%AF
    """
    crl = pycurl.Curl()
    crl.setopt(pycurl.FOLLOWLOCATION, 0)
    crl.setopt(pycurl.MAXREDIRS, 5)
    crl.setopt(pycurl.ENCODING,"gzip,deflate")
    crl.setopt(pycurl.POST, 1)
    crl.setopt(pycurl.POSTFIELDS,  json.dumps(json_message,ensure_ascii=False).encode('utf-8'))
    crl.setopt(pycurl.CONNECTTIMEOUT, 6)
    crl.setopt(pycurl.TIMEOUT, 15)
    crl.setopt(pycurl.SSL_VERIFYPEER,False)
    crl.fp = StringIO()
    crl.setopt(pycurl.URL, ("https://api.weixin.qq.com/cgi-bin/message/custom/send?access_token=%s"%token).encode('utf-8'))
    crl.setopt(crl.WRITEFUNCTION, crl.fp.write)
    crl.perform()
    res_code=crl.getinfo(pycurl.HTTP_CODE)
    res_body=json.loads(crl.fp.getvalue())
    crl.close()
    return res_body
def DeleteMemu(token):
    req=urllib2.Request('https://api.weixin.qq.com/cgi-bin/menu/delete?access_token=%s'%token)
    return urllib2.urlopen(req).read()
def SetMenu(token,menu_json):
    url = 'https://api.weixin.qq.com/cgi-bin/menu/create?access_token=%s'%token
    crl = pycurl.Curl()
    crl.setopt(pycurl.FOLLOWLOCATION, 1)
    crl.setopt(pycurl.MAXREDIRS, 5)
    crl.setopt(pycurl.AUTOREFERER,1)
    crl.setopt(pycurl.SSL_VERIFYHOST,0)
    crl.setopt(pycurl.SSL_VERIFYPEER,0)

    crl.setopt(pycurl.CONNECTTIMEOUT, 60)
    crl.setopt(pycurl.TIMEOUT, 300)
    #crl.setopt(pycurl.PROXY,proxy)
    crl.setopt(pycurl.HTTPPROXYTUNNEL,1)
    crl.fp = StringIO()
    crl.setopt(crl.POSTFIELDS,  json.dumps(menu_json,ensure_ascii=False).encode('utf-8'))
    crl.setopt(pycurl.URL, url.encode('utf-8'))
    crl.setopt(crl.WRITEFUNCTION, crl.fp.write)
    crl.perform()

    return json.loads(crl.fp.getvalue())
def GetUserInfo(token,openid):
    request = urllib2.Request("https://api.weixin.qq.com/cgi-bin/user/info?access_token=%s&openid=%s&lang=zh_CN"%(token,openid))
    data=json.loads(urllib2.urlopen(request).read())
    return data
def GetUserWatch(token):
    all_follow=set()
    next_openid=''
    while True:
        request = urllib2.Request("https://api.weixin.qq.com/cgi-bin/user/get?access_token=%s&next_openid=%s"%(token,next_openid))
        data=json.loads(urllib2.urlopen(request).read())
        if data['count']==0:
            break
        next_openid=data.get('next_openid','')
        openidlist=data['data']['openid']
        all_follow.update(openidlist)
        if next_openid=='':
            break
    return all_follow
def CreateQRCode(token,scene_id,expire_seconds=None):
    if expire_seconds:
        postdata={"expire_seconds": expire_seconds, "action_name": "QR_SCENE", "action_info": {"scene": {"scene_id": scene_id}}}
    else:
        postdata={"action_name": "QR_LIMIT_SCENE", "action_info": {"scene": {"scene_id": scene_id}}}
    request = urllib2.Request("https://api.weixin.qq.com/cgi-bin/qrcode/create?access_token=%s"%(token),json.dumps(postdata))
    data=json.loads(urllib2.urlopen(request).read())
    ticket=data['ticket']
    return "https://mp.weixin.qq.com/cgi-bin/showqrcode?ticket=%s"%ticket
if __name__ == '__main__' :
    token=GetAccessToken()
    print(token)
    data=PostFile(token,r'D:\desktop\201402120700314c6c8.jpg')
    print data
    data=GetFile(token,data)
    print(data)
