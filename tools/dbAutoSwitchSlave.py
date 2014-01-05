from sqlalchemy.orm import Session
import random

class RoutingSession(Session):
    def __init__(self,**kwargs):
        kwargssuper=kwargs.copy()
        del kwargssuper['slave_bind']
        super(RoutingSession, self).__init__(**kwargssuper)
        self.slave_bind=kwargs.get('slave_bind',[])
    def get_bind(self, mapper=None, clause=None ):
        if self._flushing:
            return self.bind
        else:
            if self.slave_bind:
                return random.choice(self.slave_bind)
            else:
                return self.bind
    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()