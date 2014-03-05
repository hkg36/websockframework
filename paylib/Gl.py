#!-*- coding:utf-8 -*-
'''
Created on 2013-6-15

@author: shangwei
'''
from tools.helper import script_path
import os
'''
全局变量
'''
from Crypto.PublicKey import RSA
'''
publickey为易宝的公钥
privatekey为商户自己的私钥
'''
path=script_path()
publickey = RSA.importKey(open(os.path.join(path,'rsa_public_key144.pem'),'r').read())
privatekey=RSA.importKey(open(os.path.join(path,'pkcs8_rsa_private_key144.pem'),'r').read())
merchantaccount='YB01000000144'
URL='mobiletest.yeepay.com'