#coding:utf-8
import urllib2
import urllib
import json

sm="感谢您注册%s，您的验证码是%s【%s】"%('来信','9980','成都来福思')
if isinstance(sm,unicode):
    sm=sm.encode('utf-8')
data = {'apikey': 'a504a679f1a11dcd150cef275642a7e2',
        'mobile':'18072846927',
        'text':sm
       }
res=urllib2.urlopen('http://yunpian.com/v1/sms/send.json',urllib.urlencode(data))
print res.code
result=json.loads(res.read())
print json.dumps(result,ensure_ascii=False)
