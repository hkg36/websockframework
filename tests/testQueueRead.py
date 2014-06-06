from kombu import Connection,Exchange, Consumer, Queue

Queue_User="guest"
Queue_PassWord="guest"
Queue_Server='192.173.1.213'
Queue_Port=5672
Queue_Path='/websocketserver'

def callback(body, message):
    print body,message.headers
connection = Connection(hostname=Queue_Server,port=Queue_Port,userid=Queue_User,password=Queue_PassWord,virtual_host=Queue_Path)
channel = connection.channel()
smsExchange=Exchange("system",type='topic',channel=channel,durable=True,delivery_mode=2)
task_queue = Queue('test_recv',exchange=smsExchange,routing_key='sys.paylog',durable=False,channel=channel)
consumer = Consumer(channel,task_queue,no_ack=True,callbacks=[callback])
consumer.qos(prefetch_count=1)
consumer.consume()
while True:
    connection.drain_events()
connection.close()
