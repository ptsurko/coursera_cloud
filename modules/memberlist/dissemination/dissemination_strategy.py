
import abc

class DisseminationStrategy():
    __metaclass__ = abc.ABCMeta
    
    @abc.abstractmethod
    def disseminate(self, memberlist):
        pass 