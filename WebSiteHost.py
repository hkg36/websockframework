#coding:utf-8
import web

from WebSiteBasePage import LoadPageList

web.config.debug = False
path_list=LoadPageList()
webapp=web.application(path_list, locals())
del path_list
application = webapp.wsgifunc()
