
from proto.rpc.server.baseserver import BaseServer
from proto.rpc.server.handlers import RpcServiceHandler
from proto.rpc.server.error_message import ErrorMessage
from proto.serializer import Serializer
from proto.rpc._rpcrequest import _RpcRequestSerializer
from proto.rpc.server.baseserver import ServerException

# TODO:
# - reorganize code to have client/server modules
# - hide service/method descriptor
# - add blocking/non-blocking listening

class RpcServer(BaseServer):
    _descriptor = None
    
    def __init__(self, service=None, *args, **kwargs):
        super(RpcServer, self).__init__(*args, **kwargs)
        
        self._service_handlers = []
        if service is not None:
            self.add_handler_for_service(service)
        
    def add_handler(self, handler):
        raise Exception('\add_handler\' is not supported, use \'add_handler_for_service\' instead')
    
    def add_handler_for_service(self, service):
        self._service_handlers.append(RpcServiceHandler(service))
    
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