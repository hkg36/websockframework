import WebSiteBasePage
import web
import dbconfig
from datamodel.connection_info import ConnectionInfo
import QueuePush

Queue_User="guest"
Queue_PassWord="guest"
Queue_Server='127.0.0.1'
Queue_Port=None
Queue_Path='/websocketserver'

pusher=QueuePush.QueuePush(Queue_Server,Queue_Port,Queue_User,Queue_PassWord,Queue_Path)

class MainPage(WebSiteBasePage.AutoPage):
    def GET(self):
        return self.buildpage()
    def POST(self):
        post_params=web.input()
        post_data=post_params['content']
        session=dbconfig.Session()
        conn_info=session.query(ConnectionInfo).filter(ConnectionInfo.client_id==post_params['id']).first()
        pusher.Push(conn_info.queue_id,conn_info.connection_id,post_data)
        return self.buildpage()
    def buildpage(self):
        session=dbconfig.Session()
        idlist=[]
        for conninfo in session.query(ConnectionInfo).all():
            idlist.append(conninfo.client_id)
        tpl=WebSiteBasePage.jinja2_env.get_template('Main.html')
        return tpl.render(idlist=idlist)