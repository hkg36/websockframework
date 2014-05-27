__author__ = 'amen'
import json
def FunctionShell(timeout=30):
    def ACF(fun):
        def Work(*args,**kwargs):
            print dir(fun)
            print '%s.%s(%s,%s)'%(fun.__module__,fun.__name__,json.dumps(args),json.dumps(kwargs))
            return fun(*args,**kwargs)
        return Work
    return ACF

@FunctionShell()
def PP(aa,bb=2):
    return aa*bb