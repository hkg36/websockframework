#coding:utf-8
import WebSiteBasePage
import web
import markdown2
import codecs

__author__ = 'amen'
class Explanation(WebSiteBasePage.AutoPage):
    def GET(self):
        input_file = codecs.open("templates/Explanation.md", mode="r", encoding="utf-8")
        text = input_file.read()

        tpl=WebSiteBasePage.jinja2_env.get_template('ShowMarkDown.html')
        return tpl.render(content=text)