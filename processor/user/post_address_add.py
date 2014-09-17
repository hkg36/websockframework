from datamodel.user import UserPostAddress
from tools.helper import Res
from tools.session import CheckSession

__author__ = 'amen'
import BackEndEnvData
import dbconfig


@CheckSession()
def run(province,city,zone,detail,phone,name,addrid=None):
    with dbconfig.Session() as session:
        upa=UserPostAddress()
        if addrid:
            upa.addrid=addrid
        upa.uid=BackEndEnvData.uid
        upa.province=province
        upa.city=city
        upa.zone=zone
        upa.detail=detail
        upa.phone=phone
        upa.name=name
        upa=session.merge(upa)
        session.commit()

        return Res({"addrid":upa.addrid})

