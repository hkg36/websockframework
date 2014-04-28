import websocket
ws = websocket.create_connection("wss://service.laixinle.com:8002/ws")
while True:
    print ws.recv()
