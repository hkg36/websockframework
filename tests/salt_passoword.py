import random
import hashlib
import base64
def make_salt_pass(password,salt_len=10):
    salt=""
    for i in xrange(1,salt_len):
        salt+=random.choice("1234567890qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM")
    pass_add_salt=password+salt
    return "saltsha256$"+salt+"$"+base64.b64encode(hashlib.sha256(pass_add_salt).digest())

def check_salt_pass(password,saltpass):
    try:
        sps=saltpass.split("$")
        if sps[0]=="saltsha256":
            pass_add_salt=password+sps[1]
            sc1=base64.b64decode(sps[2])
            return hashlib.sha256(pass_add_salt).digest()==sc1
        return False
    except:
        return False

print(make_salt_pass("sdadse"))
print(check_salt_pass("sdadse","saltsha256$nqv4GCYUs$TeZtV4W7XBNSjSjv0U/Q7R8pR0cROBWj/y8Z8CHS4sY="))