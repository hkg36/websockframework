#coding:utf-8
import datetime

import qiniu.rsf
import qiniu.conf
import qiniu.rs


qiniu.conf.ACCESS_KEY = "x5yGWWp6fBGMwlJyEU0GVzilkNIa7Mc87ibrKpdU"
qiniu.conf.SECRET_KEY = "r_8i1p4LCaiI0isFxuF2paAKhoQotGeqngCD4B1O"
qiniuSpace="kidswant"

beforetime=datetime.datetime(year=2014,month=3,day=10)
todel_file=[]

rs = qiniu.rsf.Client()
marker = None
err = None
while err is None:
    ret, err = rs.list_prefix(qiniuSpace, prefix="", limit=1000, marker=marker)
    marker = ret.get('marker', None)
    for item in ret['items']:
        dtime=datetime.datetime.fromtimestamp(item['putTime']/10e6)
        timedelta=dtime-beforetime
        if timedelta.total_seconds()<0:
            todel_file.append(item)
if err is not qiniu.rsf.EOF:
    # 错误处理
    pass

delkeys=[]
for delf in todel_file:
    path_1 = qiniu.rs.EntryPath(qiniuSpace, delf['key'])
    delkeys.append(path_1)
rets, err = qiniu.rs.Client().batch_delete(delkeys)
print(rets)