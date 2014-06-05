from datamodel.events import Events
from datamodel.message import Message

__author__ = 'amen'
import dbconfig
import time
import datetime


def DataClean():
    deadline=datetime.datetime.now()-datetime.timedelta(days=60)
    with dbconfig.Session() as session:
        session.query(Message).filter(Message.time<deadline).delete()
        session.query(Events).filter(Events.create_time<deadline).delete()
        session.commit()

DataClean()

