__author__ = 'amen'

try:
    import ujson as json
except Exception,e:
    import json
import BackEndEnvData
import dbconfig
from datamodel.connection_info import ConnectionInfo
def run(id):
    conninfo=ConnectionInfo()
    conninfo.client_id=int(id)
    conninfo.connection_id=BackEndEnvData.connection_id
    conninfo.queue_id=BackEndEnvData.reply_queue

    session=dbconfig.Session()
    session.merge(conninfo)
    session.commit()
    return {"reged":id}
