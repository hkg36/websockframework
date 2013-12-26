__author__ = 'amen'
import BackEndEnvData
import json
import anyjson
from datamodel.tools.json_encode import new_alchemy_encoder
def AddPostPublish(newpost):
    try:
        json_post=json.dumps(newpost, cls=new_alchemy_encoder(), check_circular=False)
    except Exception,e:
        print e
        return
    BackEndEnvData.queue_producer.publish(body=json_post,delivery_mode=2,
                                      routing_key='sys.post_to_notify',
                                      compression='gzip')
def AddMessageTrans(newmessage):
    try:
        json_msg=anyjson.dumps(newmessage.toJson())
    except Exception,e:
        print e
        return
    BackEndEnvData.queue_producer.publish(body=json_msg,delivery_mode=2,
                                        routing_key='sys.message_to_notify',
                                        compression='gzip')