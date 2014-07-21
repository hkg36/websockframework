#coding:utf-8
import urllib
import pycurl
from StringIO import StringIO

from lxml import etree

phone='18072846927'
msg = urllib.quote(u'您的莱信验证码为:5678，请在5分钟内输入完成验证'.encode('utf-8'))
curl=pycurl.Curl()
curl.fp = StringIO()
curl.setopt(pycurl.URL, ("http://utf8.sms.webchinese.cn/?Uid=laifusi&Key=5be675cc08e2909f9f36&smsMob=%s&smsText=%s"%
                        (phone,msg)).encode())
#curl.setopt(pycurl.URL, ("http://60.191.57.85:8881/sms.aspx?account=771005&password=3F7J4C56&mobile=%s&content=%s&action=send&sendTime=&extno="%
                        #(phone,msg)).encode())
#curl.setopt(pycurl.URL, "http://60.191.57.85:8881/sms.aspx?account=771005&password=3F7J4C56&action=overage")
curl.setopt(curl.WRITEFUNCTION, curl.fp.write)
curl.perform()
curl.fp.seek(0)
result=curl.fp.read()
print result