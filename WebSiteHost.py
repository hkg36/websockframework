#coding:utf-8
import web
from jinja2 import Environment, FileSystemLoader
env = Environment(loader=FileSystemLoader('templates'))

class hello:
    def GET(self):
        return "hello word day"
urls = (
    '/.*', hello,
    )
webapp=web.application(urls, globals())
web.config.debug = False
application = webapp.wsgifunc()