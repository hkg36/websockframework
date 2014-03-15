from mongoengine import Q
from datamodel.user import UserExData
from tools.helper import Res
from tools.session import CheckSession

__author__ = 'amen'
import BackEndEnvData
import dbconfig

SEARCH_R=0.03
@CheckSession()
def run(alltag,lat=None,long=None):
    findparams=Q(tags__all=alltag)
    if lat is not None and long is not None:
        findparams=findparams and Q(position__geo_within_sphere=[(long,lat),SEARCH_R])
    ulist=[]
    for user in UserExData.objects(findparams).order_by('-update_time').limit(300):
        ulist.append({"uid":user.uid,"tags":user.tags,"lat":user.position['coordinates'][1],
                "long":user.position['coordinates'][0],'time':user.update_time})
    return Res({'users':ulist})