import cStringIO
import sys

from field_type import FieldType
from _field_descriptor import _FieldDescriptor
from proto._tokenizer import _Tokenizer

class Serializer(object):
    _message_descriptors = {}
    
    @classmethod
    def register_message_descriptor(cls, message_class, descriptor):
        cls._message_descriptors[message_class] = descriptor
    
    @classmethod
    def serialize(cls, message):
        if message._descriptor is None:
            raise SerializerException('Message %s does not have associated descriptor.' % message.__class__.__name__)
        
        descriptor = message.get_descriptor()
        tokenizer = _Tokenizer()
        
        output_str = cStringIO.StringIO()
        
        try:
            cls._write_object(tokenizer, output_str, descriptor, message)
        except Exception as e:
            raise SerializerException('Serialization error: %s.' % e.message), None, sys.exc_info()[2]
            
        return output_str.getvalue()
    
    @classmethod
    def can_deserialize(cls, string, message_class):
        try:
            cls.deserialize(string, message_class)
            return True
        except: 
            return False
    
    @classmethod
    def deserialize(cls, string, message_class):
        if message_class not in cls._message_descriptors:
            raise Exception('Message %s does not have associated descriptor.' % message_class)
        
#         descriptor = cls._message_descriptors[message_class]
        tokenizer = _Tokenizer()
        
        string_stream = cStringIO.StringIO(string) if not isinstance(string, cStringIO.InputType) else string
        
        try:
            return cls._read_object(tokenizer, string_stream, message_class)
        except Exception as e:
            raise SerializerException('Deserialization error: %s.' % e.message), None, sys.exc_info()[2]
        
    
    @classmethod
    def _write_field(cls, tokenizer, output_str, descriptor, value):
        if descriptor.type == FieldType.String:
            tokenizer.write_int(output_str, len(value), FieldType.Int32)
            tokenizer.write_str(output_str, value)
        elif descriptor.type >= FieldType.Int8 and descriptor.type <= FieldType.Int64:
            tokenizer.write_int(output_str, value, descriptor.type)
        elif descriptor.type == FieldType.List:
            tokenizer.write_int(output_str, len(value), FieldType.Int32)
            if descriptor.list_item_type != FieldType.Object:
                list_item_descriptor = _FieldDescriptor(None, descriptor.list_item_type)
                for item in value:
                    cls._write_field(tokenizer, output_str, list_item_descriptor, item)
            else:
                for item in value:
                    cls._write_object(tokenizer, output_str, descriptor.list_item_class.get_descriptor(), item)
        elif descriptor.type == FieldType.Object:
            cls._write_object(tokenizer, output_str, descriptor.object_class.get_descriptor(), value)
            
    
    @classmethod
    def _write_object(cls, tokenizer, output_str, descriptor, value):
        for field in descriptor.fields:
            cls._write_field(tokenizer, output_str, field, getattr(value, field.name))
    
    @classmethod    
    def _read_field(cls, tokenizer, input_str, descriptor):
        if descriptor.type == FieldType.String:
            str_len = tokenizer.read_int(input_str, FieldType.Int32)
            return tokenizer.read_str(input_str, str_len)
        elif descriptor.type >= FieldType.Int8 and descriptor.type <= FieldType.Int64:
            return tokenizer.read_int(input_str, descriptor.type)
        elif descriptor.type == FieldType.List:
            array_len = tokenizer.read_int(input_str, FieldType.Int32)
            array = []
            if descriptor.list_item_class is not None:
                for _ in range(array_len):
                    array.append(cls._read_object(tokenizer, input_str, descriptor.list_item_class))
            else:
                array_item_descriptor = _FieldDescriptor(None, descriptor.list_item_type)
                for _ in range(array_len):
                    array.append(cls._read_field(tokenizer, input_str, array_item_descriptor))
            return array
            
        elif descriptor.type == FieldType.Object:
            return cls._read_object(tokenizer, input_str, descriptor.object_class)
        
    
    @classmethod
    def _read_object(cls, tokenizer, input_str, object_class):
        obj = object_class()
        for field in object_class.get_descriptor().fields:
            value = cls._read_field(tokenizer, input_str, field)
            setattr(obj, field.name, value)
        return obj
    
class SerializerException(Exception):
    pass