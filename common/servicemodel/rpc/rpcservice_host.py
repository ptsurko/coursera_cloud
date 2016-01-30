
from proto.serializer import Serializer
from common.servicemodel.service_host import ServiceHost, ServerException
from common.servicemodel.rpc._rpcrequest import _RpcRequestSerializer
from common.servicemodel.rpc.error_message import ErrorMessage

# TODO:
# - reorganize code to have client/server modules
# - hide service/method descriptor
# - add blocking/non-blocking listening

class _RpcServiceHandler():
    def __init__(self, service):
        self._service = service

    def can_handle(self, method):
        return hasattr(self._service, method)
    
    def handle(self, method, data):
        method_descriptor = getattr(self._service, method)._descriptor
        
        message = Serializer.deserialize(data, method_descriptor.request_class)

        return method_descriptor.method(self._service, message)

class RpcSericeHost(ServiceHost):
    _descriptor = None
    
    def __init__(self, service=None, *args, **kwargs):
        super(RpcSericeHost, self).__init__(*args, **kwargs)
        
        self._service_handlers = []
        if service is not None:
            self.add_handler_for_service(service)
        
#     def add_handler(self, handler):
#         raise Exception('\add_handler\' is not supported, use \'add_handler_for_service\' instead')
    
    def add_handler_for_service(self, service):
        self._service_handlers.append(_RpcServiceHandler(service))
    
    def process_request(self, address, data):
        request = _RpcRequestSerializer.deserialize(data)
        self.logger.debug('Processing \'%s\' rpc method.' % request.method)
        
        for h in self._service_handlers:
            if h.can_handle(request.method):
                response = h.handle(request.method, request.data)
                if response:
                    return Serializer.serialize(response)
                else:
                    return None
        else:
            raise ServerException('Method %s is not supported.' % request.method)
    
    def handle_error(self, address, exception, exc_info):
        self.logger.error('Unhandled error: %s' % exception.message, exc_info=exc_info)
        return Serializer.serialize(ErrorMessage(exception.message))