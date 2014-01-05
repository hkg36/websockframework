__author__ = 'amen'

try:
    import ujson as json
except Exception,e:
    import json
import BackEndEnvData
import dbconfig
from datamodel.connection_info import ConnectionInfo
def run(id):
    with dbconfig.Session() as session:
        conninfo=session.query(ConnectionInfo).filter(ConnectionInfo.connection_id==BackEndEnvData.connection_id).first()
        if conninfo is None:
            conninfo=ConnectionInfo()
        conninfo.client_id=int(id)
        conninfo.connection_id=BackEndEnvData.connection_id
        conninfo.queue_id=BackEndEnvData.reply_queue

        session.merge(conninfo)
        session.commit()
    return {"reged":id}
