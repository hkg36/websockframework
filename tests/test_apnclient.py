#coding:utf-8
from apnsclient import *

session = Session()
con = session.get_connection("push_sandbox", cert_file="debug.pem")
message = Message(["9355ecae751e0fe082a74be147de954845a2e2a25bf6c504831d74d3369f5a03"], alert=u"centos安装rabbit", badge=10)
# Send the message.
srv = APNs(con)
res = srv.send(message)
for token, reason in res.failed.items():
    code, errmsg = reason
    print "Device faled: {0}, reason: {1}".format(token, errmsg)
for code, errmsg in res.errors:
    print "Error: ", errmsg
if res.needs_retry():
    retry_message = res.retry()
