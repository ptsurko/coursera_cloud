
import abc
from enum import Enum

class _State(Enum):
    Pending = 0
    Resolved = 1
    Rejected = 2

 
class Thenable(object):
    __metaclass__ = abc.ABCMeta
    
    @abc.abstractmethod
    def then(self, onFulfilled, onRejected=None):
        pass

class Resolvable(object):
    __metaclass__ = abc.ABCMeta
    
    @abc.abstractmethod
    def resolve(self, value):
        pass
    
    @abc.abstractmethod
    def reject(self, error):
        pass

# TODO: 
class Promise(Thenable, Resolvable):
    def __init__(self):
        self._callbacks = []
        self._errbacks = []
        self._state = _State.Pending
        
        self._value = None
        self._error = None
    
    def resolve(self, value):
        if self._state != _State.Pending:
            raise PromiseException('Promise has already been ' + ('resolved' if self._state == _State.Resolved else 'rejected'))
        
        if isinstance(value, Thenable):
            value.then(self.resolve, self.reject)
        elif hasattr(value, '__call__'):
            try:
                value(self.resolve, self.reject)
            except Exception as e:
                if self._state == _State.Pending:
                    self.reject(e)
        else:
            self._state = _State.Resolved
            self._value = value
            for callback in self._callbacks:
                # TODO: handle errors in callback
                # TODO: handle returning thenable
                new_value = callback(value)
                self._value = new_value if new_value is not None else value 
                

#     def resolved(self):
#         return self._state == _State.Resolved


    def reject(self, error):
        if self._state != _State.Pending:
            raise PromiseException('Promise has already been ' + ('resolved' if self._state == _State.Rejected else 'rejected'))
        
        #TODO: handling exceptions in error callback
        
        self._state = _State.Rejected
        self._error = error
        for errback in self._errbacks:
            errback(error)
    
#     def rejected(self):
#         return self.__State == _State.Rejected
    
    
    def then(self, onFulfilled, onRejected=None):
        if self._state == _State.Resolved:
            onFulfilled()
        elif self._state == _State.Rejected and onRejected:
            onRejected()
        
        self._callbacks.append(onFulfilled)
        if onRejected:
            self._errbacks.append(onRejected)    
            
            
            
class PromiseException(Exception):
    pass