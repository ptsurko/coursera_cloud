
from cStringIO import StringIO
from proto._tokenizer import _Tokenizer

# TODO: consider using serializable attributes
class _RpcRequest(object):
    def __init__(self, service='', method='', data=''):
        self.service = service
        self.method = method
        self.data = data
        

class _RpcRequestSerializer(object):
    @classmethod
    def serialize(cls, request):
        tokenizer = _Tokenizer()

        serialized = StringIO()
        tokenizer.write_int(serialized, len(request.method))
        tokenizer.write_str(serialized, request.method)
         
        # TODO: Get rid of this len
        tokenizer.write_int(serialized, len(request.data))
        tokenizer.write_str(serialized, request.data)
         
        return serialized.getvalue()
    
    @classmethod
    def deserialize(cls, serialized):
        tokenizer = _Tokenizer()

        string = StringIO(serialized)
        method_len = tokenizer.read_int(string)
        method = tokenizer.read_str(string, method_len)

        data_len = tokenizer.read_int(string)
        data = tokenizer.read_str(string, data_len)

        return _RpcRequest('', method, data)
