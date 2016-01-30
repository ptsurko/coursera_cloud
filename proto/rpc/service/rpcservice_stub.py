from proto.rpc._method_descriptor import _MethodDescriptor
from proto.rpc._service_descriptor import _ServiceDescriptor

class RpcServiceStub(object):
    _descriptor = None

    @classmethod
    def get_descriptor(cls):
        return cls._descriptor
    
    
def handler(request_class, response_class=None):
    def func(method_obj):
        method_descriptor = _MethodDescriptor(method_obj.__name__, method_obj, request_class, response_class)
        
        method_obj._descriptor = method_descriptor
        return method_obj
    return func


def service(name=None):
    def func(class_obj):
        service_name = name if name else class_obj.__name__
        class_obj._descriptor = _ServiceDescriptor(service_name)
        return class_obj
    return func