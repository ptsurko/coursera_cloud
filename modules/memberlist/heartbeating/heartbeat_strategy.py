
import abc

class HeartbeatStrategy():
    __metaclass__ = abc.ABCMeta
    
    @abc.abstractmethod
    def heartbeat(self):
        pass 