#coding:utf-8
import urllib2,urllib
import time,random
import hashlib
from lxml import etree
import tenpay_config
class tenpay(object):
    def GetSign(self,query_args):
        query=query_args.copy()
        query.pop("sign","")
        keys=query.keys()
        keys.sort()
        allpair=[]
        for key in keys:
            value=query[key]
            if value=='':
                continue
            allpair.append(u"%s=%s"%(key,value))
        allpair.append(u"key=%s"%tenpay_config.partner_key)
        sign_str=u"&".join(allpair)
        sign_str=sign_str.encode('utf-8')
        return hashlib.md5(sign_str).hexdigest().upper()
    def GetSignAsKeyList(self,query_args,keylist):
        allpair=[]
        for key in keylist:
            value=query_args.get(key,None)
            if value=='' or value is None:
                continue
            allpair.append(u"%s=%s"%(key,value))
        allpair.append(u"key=%s"%tenpay_config.partner_key)
        sign_str=u"&".join(allpair)
        sign_str=sign_str.encode('utf-8')
        return hashlib.md5(sign_str).hexdigest().upper()

    def BuildReqStr(self,query_args):
        allpair=[]
        for key in query_args:
            value=query_args[key]
            if isinstance(value,unicode):
                allpair.append("%s=%s"%(key,urllib.quote(value.encode('utf-8'))))
            else:
                allpair.append("%s=%s"%(key,urllib.quote(str(value))))
        return "&".join(allpair)
    def init(self,billno,desc,total_fee):
        query_args = { 'ver':'2.0', 'charset':"1","bank_type":"0","desc":desc,
               "bargainor_id":tenpay_config.partner,"sp_billno":billno,"total_fee":total_fee,
               "notify_url":tenpay_config.notify_url,"callback_url":tenpay_config.callback_url,
               #"time_start":time.strftime("%Y%m%d%H%M%S",time.gmtime(time.time())),
               #"time_expire":time.strftime("%Y%m%d%H%M%S",time.gmtime(time.time()+60*20))
                }
        query_args['sign']=self.GetSign(query_args)
        data=self.BuildReqStr(query_args)
        # Send HTTP POST request
        request = urllib2.Request("https://wap.tenpay.com/cgi-bin/wappayv2.0/wappay_init.cgi" , data)

        response = urllib2.urlopen(request)

        res_tree=etree.fromstring(response.read())
        token=res_tree.xpath("//root/token_id/text()",smart_strings=False)[0]

        return token
    def VerifySign(self,query_args):
        signed=query_args.get("sign",None)
        tosign=self.GetSign(query_args)
        return tosign==signed
if __name__ == '__main__':
    tp=tenpay()
    billno="%d-%d"%(time.time(),random.randint(100,999))
    token_id= tp.init(billno,u"测试商品",1)
    print "https://wap.tenpay.com/cgi-bin/wappayv2.0/wappay_gate.cgi?token_id=%s"%token_id
