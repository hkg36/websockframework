#coding:utf-8
import apnsclient
from datamodel.ios import IOSDevice
import dbconfig
import time
import tools.APN_Tools
import logging
logging.basicConfig()

session=apnsclient.Session()
con=session.get_connection("feedback_production",certificate=tools.APN_Tools.P12Certificate(cert_file="configs/laixin_release.p12",passphrase='Laixin123'))
srv = apnsclient.APNs(con)

while True:
    with dbconfig.Session() as dbsession:
        for token,deltime in srv.feedback():
            dbsession.query(IOSDevice).filter(IOSDevice.device_token==token).delete(False)
        dbsession.commit()
    time.sleep(60*5)
