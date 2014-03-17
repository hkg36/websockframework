try:
    import ujson as json
except Exception,e:
    import json
import BackEndEnvData
import dbconfig
from datamodel.connection_info import ConnectionInfo
def run():
    with dbconfig.Session() as session:
        session.query(ConnectionInfo).filter(ConnectionInfo.queue_id==BackEndEnvData.reply_queue).delete()
        session.commit()
