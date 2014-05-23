#coding:utf-8
import urllib
from tools.helper import AutoFitJson

__author__ = 'amen'
import json

import qiniu.rs
import web

import WebSiteBasePage
import dbconfig
import datamodel.user
import website_config

class Version(WebSiteBasePage.AutoPage):
    def GET(self):
        tpl=WebSiteBasePage.jinja2_env.get_template('android/newversion.html')
        return tpl.render()
    def POST(self):
        prams=web.input(file={})
        verCode=int(prams['verCode'])
        verName=prams['verName']
        Info=prams['Info']
        file=prams['file']

        filepath=file.filename.replace('\\','/') # replaces the windows-style slashes with linux ones.
        filename=filepath.split('/')[-1] # splits the and chooses the last part (the filename with extension)
        fout = open('static/android/'+ filename,'w') # creates the file where the uploaded file should be stored
        fout.write(file.file.read()) # writes the uploaded file to the newly created file.
        fout.close() # closes the file, upload complete.

        fout=open('static/android/version.js','w')
        json.dump({'verCode':verCode,'verName':verName,'Info':Info,'url':'http://%s/static/android/%s'%(website_config.hostname,filename)},fout)
        fout.close()
        raise web.seeother('/static/android/version.js')
