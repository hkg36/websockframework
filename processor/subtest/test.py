__author__ = 'amen'
import hashlib
def run(data):
    data=data.encode('utf8')
    global reply_info
    return {'data':data,'md5':hashlib.md5(data).hexdigest(),'rep_queue':reply_info}