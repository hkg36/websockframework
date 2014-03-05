#coding:utf-8
import web

from WebSiteBasePage import LoadPageList

path_list=LoadPageList()
webapp=web.application(path_list, locals())
web.config.debug = False
application = webapp.wsgifunc()
