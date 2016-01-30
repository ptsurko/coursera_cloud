
from _basechannel import _RpcChannel

class RpcClientStub(object):
    _descriptor = None
    
    def __init__(self, address, timeout=None):
        self.channel = _RpcChannel(address, timeout=timeout)
    
    @classmethod
    def get_descriptor(cls):
        return cls._descriptor