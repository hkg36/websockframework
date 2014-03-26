#coding:utf-8
from processor.connection_lost import run as runconnlost
from tools.helper import Res

def run():
    runconnlost()
    return Res()
