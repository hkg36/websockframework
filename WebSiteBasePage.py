import os
import importlib
from jinja2 import Environment, FileSystemLoader
jinja2_env = Environment(loader=FileSystemLoader('templates'))

class AutoPage(object):
    pass

def LoadPageList(module_root='webpages'):
    pathlist=[]
    list_dirs = os.walk(module_root)
    for root, dirs, files in list_dirs:
        root_path=root.replace('/','.')
        for f in files:
            if f.endswith('.pyc') or f=='__init__.py':
                continue
            mod=importlib.import_module('.'+f[:-3],root_path)
            for name in mod.__dict__:
                tp=mod.__dict__[name]
                try:
                    if tp==AutoPage:
                        continue
                    if issubclass(tp,AutoPage):
                        path=root[len(module_root):]
                        path='%s/%s'%(path,name)
                        pathlist.extend((path,tp))
                except Exception,e:
                    pass
    return pathlist
