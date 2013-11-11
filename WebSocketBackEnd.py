__author__ = 'amen'
import QueueWorker2
import importlib
import traceback
import getopt
import sys
try:
    import ujson as json
except Exception,e:
    import json

class BackWork(QueueWorker2.QueueWorker):
    def RequestWork(self,params,body,reply_queue):
        try:
            request=json.loads(body)
        except Exception,e:
            return params,'body error:%s'%str(e)
        function=request.get("function",None)
        if function:
            function_params=request.get("params",None)
            if function_params and isinstance(function_params,dict):
                try:
                    mfunc=importlib.import_module('processor.'+function)
                except Exception,e:
                    return params,'no function'
                try:
                    mfunc.reply_info={'queueid':reply_queue,'connid':params.get('connid'),'clientip':params.get('cip')}
                    result=mfunc.run(**function_params)
                    del mfunc.reply_info
                    if 'client_code' in request and isinstance(result,dict):
                        result['client_code']=request['client_code']
                    if isinstance(result,dict) or isinstance(result,list):
                        return params,json.dumps(result)
                    elif isinstance(result,basestring):
                        return params,result
                except BaseException,e:
                    return params,traceback.format_exc()
        return params,"command format error,check again"
if __name__ == '__main__':
    Queue_User="guest"
    Queue_PassWord="guest"
    Queue_Server='127.0.0.1'
    Queue_Port=5672
    Queue_Path='/websocketserver'
    opts, args=getopt.getopt(sys.argv[1:],'h:p:u:w:a:',
                             ['queuehost=','queueport=','queueusr=','queuepsw=','queuepath='])
    for k,v in opts:
        if k in ('-h','--queuehost'):
            Queue_Server=v
        elif k in ('-p','--queueport'):
            Queue_Port=int(v)
        elif k in ('-u','--queueusr'):
            Queue_User=v
        elif k in ('-w','--queuepsw'):
            Queue_PassWord=v
        elif k in ('-a','--queuepath'):
            Queue_Path=v
    worker=BackWork(Queue_Server,Queue_Port,Queue_Path,Queue_User,Queue_PassWord,'task')
    worker.run()
