#coding:utf-8
import datetime
import json
import qiniu.rsf
import qiniu.conf
import qiniu.rs


qiniu.conf.ACCESS_KEY = "W4nYpf8HOCEyCzjLHpO0QVYGOykRucI1MIniLpgL"
qiniu.conf.SECRET_KEY = "3NRgrf8v_XHGGoWROaXYZoFYPvSeN3HnI_19eVfk"
qiniuSpace="cdmmstatic"

todel_file=[]

rs = qiniu.rsf.Client()
marker = None
err = None
while err is None:
    ret, err = rs.list_prefix(qiniuSpace, prefix="", limit=1000, marker=marker)
    marker = ret.get('marker', None)
    for item in ret['items']:
        todel_file.append("http://cdmmstatic.qiniudn.com/"+item['key'])

print json.dumps(todel_file,ensure_ascii=False,indent=2)