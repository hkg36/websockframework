__author__ = 'amen'
import hashlib
def run(data):
    data=data.encode('utf8')
    return {'data':data,'sha1':hashlib.sha1(data).hexdigest()}