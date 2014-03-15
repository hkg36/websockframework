from mongoalchemy.session import Session
from mongoalchemy.document import Document, Index
from mongoalchemy.fields import *
class User(Document):
    config_collection_name = 'users'
    email = StringField(_id=True)
    # Setting the possible values by using fields
    first_name = StringField()
    last_name = StringField()

me = User(first_name='Jeff', last_name='Jenkins', email='jeff@qcircles.net')
session = Session.connect('test1',host='mongodb://192.173.1.213:27010/')
session.insert(me)