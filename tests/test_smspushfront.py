import websocket
import json
import hashlib
private_code='JdYQIaDBRrdVKzIWgh8oGc9nURaFCCYI9U3y9LUnt0eD85a8sGQcY8Sq0k4S92cnYgrnObD4nELHPDY3n6Ni74o2bnlMFNjKmjjakCC8Q3qOTCri9YS9CtyKm6p9Umex7Dl6RKAvtygpNj35Y4MUowMOvulR5amRjeMw7ZVQV56PML5cJTJVpk9pnH6QtfrRzqQTijST'
ws = websocket.create_connection("wss://service.laixinle.com:8002/ws")
while True:
    data= ws.recv()
    getdata=json.loads(data)
    if 'ccode' in getdata:
        allstr=getdata['ccode']+private_code
        if isinstance(allstr,unicode):
            allstr=allstr.encode('utf-8')
            check=hashlib.sha256(allstr).hexdigest()
            ws.send(json.dumps({"check":check}))
    else:
        print(data)
