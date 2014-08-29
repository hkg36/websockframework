#coding:utf-8
__author__ = 'amen'
import apnsclient
import tools.APN_Tools

apn_connarg=['push_sandbox','configs/laixin_debug.p12','Laixin123']
session=apnsclient.Session()
con=session.get_connection(apn_connarg[0],certificate=tools.APN_Tools.P12Certificate(cert_file=apn_connarg[1],passphrase=apn_connarg[2]))
apnsrv = apnsclient.APNs(con)

apnmsg=apnsclient.Message(["df44dc87abb03ca7d7763a0d3e220fa30017dd2a6d19eb2fb5767672dd311e86"], alert=u"hello", badge=2)
apnsrv.send(apnmsg)