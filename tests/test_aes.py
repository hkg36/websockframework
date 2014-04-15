from Crypto.Cipher import AES
from Crypto import Random

key = b'Sixteen byte key'
iv = Random.new().read(AES.block_size)
print iv,len(iv)
cipher = AES.new(key, AES.MODE_CFB, iv)
msg = cipher.encrypt('no bb no die')
print msg,len(msg)
cipher = AES.new(key, AES.MODE_CFB, iv)
dsc = cipher.decrypt(msg)
print dsc,len(dsc)
