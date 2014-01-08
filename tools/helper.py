__author__ = 'amen'
import GeoCombine
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

def CombineGeo(long,lat):
    lat_int=int((lat+90)*10e6)
    long_int=int((long+180)*10e6)
    return GeoCombine.Combine(long_int,lat_int)

if __name__ == '__main__':
    print CombineGeo(147.9873,32.5678)