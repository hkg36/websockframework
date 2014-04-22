#coding:utf-8
import apnsclient
import configs.apn_product
from datamodel.ios import IOSDevice
import dbconfig
import time

session=apnsclient.Session()
con=session.get_connection("feedback_production",cert_string=configs.apn_product.cert_string, key_string=configs.apn_product.key_string)
srv = apnsclient.APNs(con)

while True:
    with dbconfig.Session() as dbsession:
        for token,deltime in srv.feedback():
            dbsession.query(IOSDevice).filter(IOSDevice.device_token==token).delete(False)
        dbsession.commit()
