
from common.servicemodel.rpc._method_descriptor import _MethodDescriptor
from common.servicemodel.rpc._service_descriptor import _ServiceDescriptor

def client(name=None):
    return service(name)

def method(request_class, response_class=None, one_way=False):
    def func(method_obj):
        method_descriptor = _MethodDescriptor(method_obj.__name__, method_obj, request_class, response_class)
        method_obj._descriptor = method_descriptor
        
        def decorated(self, message):
            return self.channel.call_method(method_descriptor, message)
        return decorated
    return func

def service(name=None):
    def func(class_obj):
        service_name = name if name else class_obj.__name__
        class_obj._descriptor = _ServiceDescriptor(service_name)
        return class_obj
    return func

def handler(request_class, response_class=None):
    def func(method_obj):
        method_descriptor = _MethodDescriptor(method_obj.__name__, method_obj, request_class, response_class)
        
        method_obj._descriptor = method_descriptor
        return method_obj
    return func

