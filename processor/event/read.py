from operator import and_
from datamodel.events import Events
from tools.helper import Res, LoadEvent
from tools.session import CheckSession

__author__ = 'amen'
import BackEndEnvData
import dbconfig


@CheckSession
def run(pos=0):
    with dbconfig.Session(read=True) as session:
        events=session.query(Events).filter(and_(Events.touid==BackEndEnvData.uid,Events.eid>pos))\
            .order_by(Events.eid.desc()).limit(50).all()
        eventlist=[]
        for event in events:
            eo=LoadEvent(event.toJson())
            if eo:
                eventlist.append(eo)
        return Res({'events':eventlist})