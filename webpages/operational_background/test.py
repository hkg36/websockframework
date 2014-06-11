from sqlalchemy import and_
import WebSiteBasePage
import web
from datamodel.user import User
import dbconfig

__author__ = 'amen'
class DeleteNick(WebSiteBasePage.AutoPage):
    def GET(self):
        params=web.input()
        uid=int(params.get('uid'))
        with dbconfig.Session() as session:
            user=session.query(User).filter(User.uid==uid).first()
            user.nick=None
            user=session.merge(user)
            session.commit()
            return "user %d nick reset"%user.uid
