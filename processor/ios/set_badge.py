from datamodel.ios import IOSDevice
from tools.helper import Res
from tools.session import CheckSession

__author__ = 'amen'
import BackEndEnvData
import dbconfig
@CheckSession()
def run(badge):
    with dbconfig.Session() as session:
        session.query(IOSDevice).filter(IOSDevice.uid==BackEndEnvData.uid).update({IOSDevice.badge:badge})
        session.commit()
    return Res()