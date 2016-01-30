
import socket

from proto.rpc._rpcrequest import _RpcRequest, _RpcRequestSerializer
from proto.serializer import Serializer
from proto.rpc.server.error_message import ErrorMessage
from proto.rpc.server.baseserver import ServerException

class _BaseChannel(object):
    def __init__(self, address, timeout=None):
        self.address = address
        self.sock = None
        self.timeout = timeout
        
    def connect(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.settimeout(self.timeout)
        self.sock.connect((self.address.host, self.address.port))
        
    
    def send(self, data):
        self.sock.sendall(data)
        
    def receive(self, recv_size=4096):
        received_data = ''
        while True:
            data = self.sock.recv(recv_size)
            received_data += data
            if len(data) < recv_size:
                break
        
        return received_data
    
    def close(self):
        if self.sock:
            print 'client: closing client socket'
            self.sock.close()
            self.sock = None
            
            
            
class _RpcChannel(_BaseChannel):
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
