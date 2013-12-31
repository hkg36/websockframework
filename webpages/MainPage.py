#coding:utf-8
import WebSiteBasePage
import web
import dbconfig
from datamodel.connection_info import ConnectionInfo
import QueuePush
import website_config

pusher=QueuePush.QueuePush(
    website_config.Queue_Server,
    website_config.Queue_Port,
    website_config.Queue_User,
    website_config.Queue_PassWord,
    website_config.Queue_Path)

class MainPage(WebSiteBasePage.AutoPage):
    def GET(self):
        return self.buildpage()
    def POST(self):
        post_params=web.input()
        post_data=post_params['content']
        session=dbconfig.Session()
        try:
            conn_info=session.query(ConnectionInfo).filter(ConnectionInfo.client_id==post_params['id']).first()
            if conn_info:
                pusher.Push(conn_info.queue_id,conn_info.connection_id,post_data)
                return self.buildpage()
            else:
                return self.buildpage(u'屏幕id不存在')
        except Exception,e:
            return self.buildpage(str(e))
    def buildpage(self,extinfo=''):
        session=dbconfig.Session()
        idlist=[]
        for conninfo in session.query(ConnectionInfo).all():
            idlist.append(conninfo.client_id)
        tpl=WebSiteBasePage.jinja2_env.get_template('Main.html')
        return tpl.render(extinfo=extinfo,idlist=idlist)