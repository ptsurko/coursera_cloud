from proto.rpc.client.rpcchannel import RpcChannel
from proto.rpc.service import service
from proto.rpc._method_descriptor import _MethodDescriptor

class RpcClientStub(object):
    _descriptor = None
    
    def __init__(self, address, timeout=None):
        self.channel = RpcChannel(address, timeout=timeout)
    
    @classmethod
    def get_descriptor(cls):
        return cls._descriptor
    
    
def method(request_class, response_class=None, one_way=False):
    def func(method_obj):
        method_descriptor = _MethodDescriptor(method_obj.__name__, method_obj, request_class, response_class)
        method_obj._descriptor = method_descriptor
        
        def decorated(self, message):
            return self.channel.call_method(method_descriptor, message)
        return decorated
    return func

# TODO: Consider renaming to Stub
def client(name=None):
    return service(name)