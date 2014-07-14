__author__ = 'amen'
import msgpack
import uuid
import time
from Crypto.Cipher import AES
import base64
session_crypt_key=b'7Y9VZl9M3HDmDfnb'
session_crypt_head='x\xaa\x83\xd4\xf3d\x01\xfa\xaf\x84\xfe;\xde\xd2o\x08'
def BuildCryptSession(uid):
    data=msgpack.packb([uuid.uuid4().get_bytes(),time.time(),uid])
    cipher = AES.new(session_crypt_key, AES.MODE_CFB, session_crypt_head)
    msg = cipher.encrypt(data)
    msg64=base64.b16encode(msg)
    return "SCK_"+msg64
def DecodeCryptSession(sessionid):
    if sessionid.startswith('SCK_')==False:
        return None
    try:
        msg64=sessionid[4:]
        msg=base64.b16decode(msg64)
        cipher = AES.new(session_crypt_key, AES.MODE_CFB, session_crypt_head)
        data=cipher.decrypt(msg)
        srcdata=msgpack.unpackb(data)
    except Exception,e:
        return None
    return {'uid':srcdata[2],'time':srcdata[1],'uuid':uuid.UUID(bytes=srcdata[0])}
if __name__ == '__main__':
    session= BuildCryptSession(223)
    print(session)
    print DecodeCryptSession(session)