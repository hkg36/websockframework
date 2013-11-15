import WebSiteBasePage

class HelloWorld(WebSiteBasePage.AutoPage):
    def GET(self):
        return "hello word day 2"
