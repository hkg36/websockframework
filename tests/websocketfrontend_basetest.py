#coding:utf-8
import websocket
import zlib
import json

conn=websocket.create_connection("wss://test.laixinle.com:8001/ws?usezlib=1")
conn.send(zlib.compress(json.dumps({
	"func":"subtest.test",
	"parm":{
        "data":u"okookok",
	}
})),opcode=websocket.ABNF.OPCODE_BINARY)
resdata=conn.recv()
print(zlib.decompress(resdata))
conn.close()
