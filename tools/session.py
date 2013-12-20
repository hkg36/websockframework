__author__ = 'amen'
import random

def GenSession():
    str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    for i in xrange(15):
        str+=chars[random.randint(0, length)]
    return str