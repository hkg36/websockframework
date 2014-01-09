__author__ = 'amen'
import os
import importlib
import json
import BackEndEnvData
import getopt
import sys
import QueueWork
import traceback
import datetime,time

def LoadProcFunctionList(module_root='processor'):
    pathlist={}
    list_dirs = os.walk(module_root)
    for root, dirs, files in list_dirs:
        root_path=root.replace('/','.')
        for f in files:
            if f.endswith('.pyc') or f=='__init__.py':
                continue
            mod=importlib.import_module('.'+f[:-3],root_path)
            try:
                runfunc=mod.run
                path=root[len(module_root)+1:]
                if path:
                    path='%s.%s'%(path.replace('/','.'),f[:-3])
                else:
                    path=f[:-3]
                pathlist[path]=runfunc
            except Exception,e:
                print path,str(e)
    return pathlist
function_list=None

class AutoFitJson(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj,datetime.datetime):
            return time.mktime(obj.timetuple())
        return json.JSONEncoder.default(self, obj)

def RequestWork(params,body,reply_queue):
    try:
        request=json.loads(body)
    except Exception,e:
        return params,'body error:%s'%str(e)
    function=request.get("func",None)
    if function:
        function_params=request.get("parm",None)
        if function_params is not None and isinstance(function_params,dict):
            mfunc=function_list.get(function)
            if mfunc is None:
                return params,'no function'
            try:
                BackEndEnvData.reply_queue=reply_queue
                BackEndEnvData.connection_id=params.get('connid')
                BackEndEnvData.client_ip=params.get('cip')
                result=mfunc(**function_params)
                if result is None:
                    return
                result['push']=False
                if 'cdata' in request and isinstance(result,dict):
                    result['cdata']=request['cdata']
                if isinstance(result,(dict,list)):
                    return params,json.dumps(result,ensure_ascii=False,cls=AutoFitJson)
                elif isinstance(result,basestring):
                    return params,result
            except BaseException,e:
                return params,traceback.format_exc()
    return params,"error"

if __name__ == '__main__':
    function_list=LoadProcFunctionList()

    config_model='configs.frontend'
    opts, args=getopt.getopt(sys.argv[1:],'c:',
                             ['config='])
    for k,v in opts:
        if k in ('-c','--config'):
            config_model=v
    try:
        configs=importlib.import_module(config_model)
    except Exception,e:
        print 'config error',str(e)
        exit(0)
    QueueWork.WorkFunction=RequestWork
    QueueWork.init(configs.Queue_Server,configs.Queue_Port,configs.Queue_Path,
                    configs.Queue_User,configs.Queue_PassWord,'task')
    BackEndEnvData.queue_producer=QueueWork.producer
    QueueWork.run()