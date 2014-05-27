__author__ = 'amen'
import web

def AccessControl():
    def ACF(fun):
        def Work(*args,**kwargs):

            return fun(*args,**kwargs)
        return Work
    return ACF