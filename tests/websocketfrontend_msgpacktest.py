#coding:utf-8
import websocket
import msgpack

conn=websocket.create_connection("wss://test.laixinle.com:8001/msgpack")
conn.send(msgpack.packb({
	"func":"subtest.test",
	"parm":{
        "data":u"大家好",
	}
}),opcode=websocket.ABNF.OPCODE_BINARY)
resdata=conn.recv()
try:
    print(msgpack.unpackb(resdata))
except Exception,e:
    print(resdata)
conn.close()
