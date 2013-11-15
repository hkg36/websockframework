__author__ = 'amen'
import hashlib
import BackEndEnvData
def run(data):
    data=data.encode('utf8')
    global reply_info
    return {'data':data,'md5':hashlib.md5(data).hexdigest(),'rep_queue':{'cid':BackEndEnvData.connection_id,
                                                                         'cip':BackEndEnvData.client_ip,'qid':BackEndEnvData.reply_queue}}