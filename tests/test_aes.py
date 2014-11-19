from Crypto.Cipher import AES
from Crypto import Random

class AutoClose(object):
    def __init__(self,session):
        self._session=session
    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        print self._session
with AutoClose("pppp") as ac:
    key = b'Sixteen byte key'
    iv = Random.new().read(AES.block_size)
    print iv,len(iv)
    cipher = AES.new(key, AES.MODE_CFB, iv)
    msg = cipher.encrypt('no bb no die')
    print msg,len(msg)
    cipher = AES.new(key, AES.MODE_CFB, iv)
    dsc = cipher.decrypt(msg)
    print dsc,len(dsc)
