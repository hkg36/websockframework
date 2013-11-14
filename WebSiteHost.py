#coding:utf-8
import web
import webpages
from jinja2 import Environment, FileSystemLoader
jinja2_env = Environment(loader=FileSystemLoader('templates'))

webapp=web.application(webpages.urls, globals())
web.config.debug = False
application = webapp.wsgifunc()