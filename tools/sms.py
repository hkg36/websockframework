#coding:utf-8
__author__ = 'amen'
import urllib2
CorpID = u"zxtj00098";
Pwd = u"zx383211";
urlx = "http://sdk.cdzxkj.com/"
result_code={0:"发送成功！",
             -1:"帐号未注册！",
             -2:"其他错误！",
             -4:"密码错误！",
             -5:"手机号码格式不对！",
             -6:"余额不足！",
             -7:"定时发送时间不是有效时间格式！",
             -8:"禁止10小时以内向同一手机号发送相同短信！"}
def SendSms(phone,code):
    msg=u"您的莱信验证码为:%s，请在5分钟内输入完成验证。【莱福思】"%code
    body=u"CorpID=%s&Pwd=%s&Mobile=%s&Content=%s&Cell=&SendTime="%(CorpID,Pwd,phone,msg)
    req = urllib2.Request(urlx+"Send.aspx",headers={"Content-Type":"application/x-www-form-urlencoded"})
    req.data=body.encode('gb2312')
    response=urllib2.urlopen(req)
    rescode=int(response.read())
    return rescode,result_code.get(rescode)
if __name__ == '__main__':
    SendSms("18072846927",2346)