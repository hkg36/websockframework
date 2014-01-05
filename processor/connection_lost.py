try:
    import ujson as json
except Exception,e:
    import json
import BackEndEnvData
import dbconfig
from datamodel.connection_info import ConnectionInfo
def run():
    with dbconfig.Session() as session:
        session.query(ConnectionInfo).filter(ConnectionInfo.connection_id==BackEndEnvData.connection_id).delete()
        session.commit()
