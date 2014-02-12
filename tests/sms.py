#coding:utf-8
import urllib
import pycurl
from StringIO import StringIO

from lxml import etree


msg = urllib.quote(u'您的莱信验证码为:5678，请在5分钟内输入完成验证。【莱福思】'.encode('utf-8'))
curl=pycurl.Curl()
curl.fp = StringIO()
#curl.setopt(pycurl.URL, "http://60.191.57.85:8881/sms.aspx?account=771005&password=3F7J4C56&mobile=18072846927&content=%s&action=send&sendTime=&extno="%msg)
curl.setopt(pycurl.URL, "http://60.191.57.85:8881/sms.aspx?account=771005&password=3F7J4C56&action=overage")
curl.setopt(curl.WRITEFUNCTION, curl.fp.write)
curl.perform()
curl.fp.seek(0)
result=curl.fp.read()
doc=etree.fromstring(result)
status=doc.xpath('/returnsms/returnstatus/text()')[0]
remain=doc.xpath('/returnsms/remainpoint/text()')[0]

print status,remain