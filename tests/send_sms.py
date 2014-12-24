#coding:utf8
import urllib2,urllib

url = "http://202.85.215.157:8888/LifeStyleMessageService/SendMessage.do"
data = urllib.urlencode({"deviceID":"APP",
	"phone":"15882117849;18618149548",
	"type":"TRX",
	"content":"您的川妹妹验证码为:7250，请在5分钟内输入完成验证."})
req = urllib2.Request(url)
fd = urllib2.urlopen(req,data)
print fd.read()