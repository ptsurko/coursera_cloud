import abc

from proto.serializer import Serializer

class BaseHandler(object):
    __metadata__ = abc.ABCMeta
    
    @abc.abstractmethod
    def can_handle(self, data):
        pass
    
    @abc.abstractmethod
    def handle(self, data):
        pass


class RpcServiceHandler():
    def __init__(self, service):
        self._service = service

    def can_handle(self, method):
        return hasattr(self._service, method)
    
    def handle(self, method, data):
        method_descriptor = getattr(self._service, method)._descriptor
        
        message = Serializer.deserialize(data, method_descriptor.request_class)

        return method_descriptor.method(self._service, message)
