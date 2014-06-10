#coding:utf-8
from sqlalchemy import and_
from datamodel.user import User,UserExData
from datamodel.user_circle import UserCircle, CircleDef, CircleRole
from tools.helper import Res, FunctionCache
from tools.session import CheckSession
import dbconfig
from tools.with_cache import GetUserInfo


def run(uid):
    return Res(GetUserInfo(uid))