__author__ = 'amen'

from mongoengine import *
import user_circle
import datetime

class GroupPost(Document):
    postid=SequenceField(primary_key=True)
    uid=LongField(required=True)
    gid=IntField(required=True)
    content=StringField()
    pictures=ListField(URLField())
    video=URLField()
    videolen=IntField()
    voice=URLField()
    voicelen=IntField()
    position=PointField()
    likes=ListField(EmbeddedDocumentField(user_circle.LikeRecord))
    replys=ListField(EmbeddedDocumentField(user_circle.ReplyRecord))
    time=DateTimeField(default=datetime.datetime.now)
    meta = {
        'indexes': ["uid",("gid","-postid")]
    }
    def toJson(self):
        data= {
            "postid":self.postid,
            "uid":self.uid,
            "gid":self.gid,
            "time":self.time,
            'likes':[one.toJson() for one in self.likes],
            'replys':[one.toJson() for one in self.replys]
        }
        if self.content:
            data["content"]=self.content
        if self.pictures:
            data['pictures']=[one for one in self.pictures]
        if self.video:
            data['video']=self.video
            data['videolen']=self.videolen
        if self.voice:
            data['voice']=self.voice
            data['voicelen']=self.voicelen
        if self.position:
            if isinstance(self.position,(list,tuple)):
                data["position"]={'lat':self.position[1],
                                  "long":self.position[0]}
            else:
                data["position"]={'lat':self.position['coordinates'][1],
                                  "long":self.position['coordinates'][0]}
        return data
