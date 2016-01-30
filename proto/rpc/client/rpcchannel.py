from basechannel import BaseChannel
from proto.rpc._rpcrequest import _RpcRequest, _RpcRequestSerializer
from proto.serializer import Serializer
from proto.rpc.server.error_message import ErrorMessage
from proto.rpc.server.baseserver import ServerException

class RpcChannel(BaseChannel):
    def __init__(self, address, timeout=None):
        super(self.__class__, self).__init__(address, timeout)
        
    def call_method(self, method_descriptor, message):
        try:
            message_data = Serializer.serialize(message)
            request = _RpcRequest('', method_descriptor.name, message_data)
            
            serialized = _RpcRequestSerializer.serialize(request)
            
            self.connect()
            self.send(serialized)
            if method_descriptor.response_class:
                response = self.receive()
                
                if Serializer.can_deserialize(response, ErrorMessage):
                    deserialized = Serializer.deserialize(response, ErrorMessage)
                    raise ServerException(deserialized.message)
                else:
                    return Serializer.deserialize(response, method_descriptor.response_class)
        finally:
            self.close()
