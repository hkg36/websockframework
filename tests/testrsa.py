#coding:utf-8
from Crypto import Random
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA,SHA256
from base64 import b64encode, b64decode
import os
private = RSA.generate(2048, os.urandom)
public=private.publickey()
print private.exportKey("PEM")
print public.exportKey("PEM")

rsakey = PKCS1_OAEP.new(public)
encrypted = rsakey.encrypt("you are a fool")
print encrypted
rsapub=PKCS1_OAEP.new(private)
print rsapub.decrypt(encrypted)


data='we are fools'
h=SHA256.new(data)
signer = PKCS1_v1_5.new(private)
signature = signer.sign(h)
print signature

checker=PKCS1_v1_5.new(public)
h=SHA256.new(data)
print checker.verify(h,signature)