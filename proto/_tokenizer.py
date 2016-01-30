from common.deprecated import deprecated
from enum import IntEnum
from field_type import FieldType

_INT_TO_LEN_MAP = {
    FieldType.Int8:1,
    FieldType.Int16:2,
    FieldType.Int32:4,
    FieldType.Int64:8,
}

class _WireTypes(IntEnum):
    VAR_INT = 0
    LENGTH_DELIMITED = 1

#TODO: consider more optimal way to work with bytes
class _Tokenizer(object):
    def write_varint(self, output_string, num):
        while True:
            num, mod = divmod(num, 128)
            if num == 0:
                output_string.write(chr(mod))
                break
            else:
                output_string.write(chr(mod + 128))
                
    def read_varint(self, input_string):
        result = 0
        while True:
            byte = ord(input_string.read(1))
            if byte & 128 == 128:
                result = (result << 8) + (byte - 128)
            else:
                return (result << 8) + byte
    
    def write_key(self, output_string, wire_type, field_number):
        output_string.write(chr((field_number << 1) % 256 + int(wire_type)))
        
    def read_key(self, input_string):
        byte = ord(input_string.read(1))
        return (byte >> 1, _WireTypes(byte % 2))
        
        
        
    @deprecated
    def write_int(self, output_string, num, num_type=FieldType.Int8):
        output_string.write(self._num_to_str(num, num_type))
    
    @deprecated
    def write_str(self, output_string, string):
        output_string.write(string)
    
    @deprecated
    def read_int(self, input_string, num_type=FieldType.Int8):
        if num_type in _INT_TO_LEN_MAP.iterkeys():
            str_len = _INT_TO_LEN_MAP[num_type]
        else:
            raise Exception('Type %r is not numeric.' % num_type)
        
        return self._str_to_num(input_string.read(str_len))
    
    @deprecated
    def read_str(self, input_string, length):
        return input_string.read(length)
    
    @deprecated
    def _str_to_num(self, string):
        result = 0
        for i, byte in enumerate(reversed(string)):
            result += ord(byte) * 256 ** i
        return result
    
    @deprecated
    def _num_to_str(self, num, num_type):
        result = ''
        a = num
        while a != 0:
            a, b = divmod(a, 256)
            result = chr(b) + result
        
        if num_type in _INT_TO_LEN_MAP.iterkeys():
            str_len = _INT_TO_LEN_MAP[num_type]
#         else:
#             raise Exception("Byte representation of %d - %d is greater that %d" % (num, len(result), str_len))
         
        return chr(0) * (str_len - len(result)) + result 