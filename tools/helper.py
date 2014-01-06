__author__ = 'amen'
def Res(res={},errno=0,error='no error'):
    return {"errno":errno,"error":error,"result":res}
def GetFileLink(db_file_record):
    return db_file_record

def LoadEvent(event):
    event_type=event['type']
    if event_type=='add_friend':
        return {'eid':event['eid'],
                'create_time':event['create_time'],
                'type':event_type,
                'uid':event['param1']}
    elif event_type=='group_invite':
        return  {'eid':event['eid'],
                'create_time':event['create_time'],
                'type':event_type,
                'gid':event['param1'],
                'fromuid':event['param2']}