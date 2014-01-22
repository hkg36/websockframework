from datamodel.ios import IOSDevice
from tools.helper import Res
from tools.session import CheckSession

__author__ = 'amen'
import BackEndEnvData
import dbconfig
@CheckSession()
def run(device_token,is_debug):
    with dbconfig.Session() as session:
        device=IOSDevice()
        device.uid=BackEndEnvData.uid
        device.device_token=device_token
        device.is_debug=is_debug
        session.merge(device)
        session.commit()
    return Res()