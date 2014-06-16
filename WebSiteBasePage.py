import os
import importlib

from jinja2 import Environment, FileSystemLoader
import web

jinja2_env = Environment(loader=FileSystemLoader('templates'),auto_reload=False)

class AutoPage(object):
    def SetNoCache(self):
        web.header('Cache-Control','no-cache, no-store, must-revalidate',unique=True)
        web.header('Pragma','no-cache',unique=True)
        web.header('Expires','0',unique=True)

def LoadPageList(module_root='webpages'):
    pathlist=[]
    list_dirs = os.walk(module_root)
    for root, dirs, files in list_dirs:
        root_path=root.replace(os.path.sep,'.')
        for f in files:
            if f.endswith('.pyc') or f=='__init__.py':
                continue
            mod=importlib.import_module(root_path+'.'+f[:-3])
            for name in mod.__dict__:
                tp=mod.__dict__[name]
                try:
                    if tp==AutoPage:
                        continue
                    if issubclass(tp,AutoPage):
                        path=root[len(module_root):]
                        path='%s/%s'%(path.replace(os.path.sep,'/'),name)
                        pathlist.extend((path,tp))
                except Exception,e:
                    pass
    return pathlist
