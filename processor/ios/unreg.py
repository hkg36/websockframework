from datamodel.ios import IOSDevice
from tools.helper import Res
from tools.session import CheckSession

__author__ = 'amen'
import BackEndEnvData
import dbconfig
@CheckSession
def run():
    with dbconfig.Session() as session:
        session.query(IOSDevice).filter(IOSDevice.uid==BackEndEnvData.uid).delete()
        session.commit()
    return Res()
