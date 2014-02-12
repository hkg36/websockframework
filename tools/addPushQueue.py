#coding:utf-8
from tools.helper import AutoFitJson

__author__ = 'amen'
import BackEndEnvData
import json


def AddPostPublish(newpost):
    json_post=json.dumps(newpost,cls=AutoFitJson,ensure_ascii=False)
    BackEndEnvData.queue_producer.publish(body=json_post,delivery_mode=2,
                                      routing_key='sys.post_to_notify',
                                      compression='gzip')
def AddMessageTrans(newmessage):
    json_msg=json.dumps(newmessage,cls=AutoFitJson,ensure_ascii=False)
    BackEndEnvData.queue_producer.publish(body=json_msg,delivery_mode=2,
                                        routing_key='sys.message_to_notify',
                                        compression='gzip')
def AddPhoneBookUpdated(uid):
    json_msg=json.dumps({'uid':uid})
    BackEndEnvData.queue_producer.publish(body=json_msg,delivery_mode=2,
                                        routing_key='sys.user_phonebook_update',
                                        compression='gzip')
def AddEventNotify(event):
    json_msg=json.dumps(event.toJson(),cls=AutoFitJson,ensure_ascii=False)
    BackEndEnvData.queue_producer.publish(body=json_msg,delivery_mode=2,
                                        routing_key='sys.event',
                                        compression='gzip')
def AddReplyNotify(reply):
    json_msg=json.dumps(reply.toJson(),cls=AutoFitJson,ensure_ascii=False)
    BackEndEnvData.queue_producer.publish(body=json_msg,delivery_mode=2,
                                        routing_key='sys.newreply',
                                        compression='gzip')
def AddLikeNotify(postlike):
    json_msg=json.dumps(postlike.toJson(),cls=AutoFitJson,ensure_ascii=False)
    BackEndEnvData.queue_producer.publish(body=json_msg,delivery_mode=2,
                                        routing_key='sys.newlike',
                                        compression='gzip')