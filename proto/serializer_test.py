
import unittest
from cStringIO import StringIO
from field_type import FieldType
from message import Message
from serializable import serializable, field
from serializer import Serializer

@serializable()
@field('int1', FieldType.Int8)
@field('str1', FieldType.String)
@field('int2', FieldType.Int16)
@field('str2', FieldType.String)
@field('int3', FieldType.Int32)
@field('int4', FieldType.Int64)
@field('array1', FieldType.List, list_item_type=FieldType.Int16)
class TestMessage1(Message):
    def __init__(self):
        self.int1 = 0
        self.str1 = ''
        self.int2 = 0
        self.str2 = '' 
        self.int3 = 0
        self.int4 = 0
        self.array1 = []
        
# @serializable()
# @field('int6', FieldType.Int8)
# @field('str7', FieldType.String)
# class TestMessage2(Message):
#     def __init__(self, int6=0, str7=''):
#         self.int6 = int6
#         self.str7 = str7

class SerializerTest(unittest.TestCase):
    def createTestMessage(self):
        m = TestMessage1()
        m.int1 = 8
        m.str1 = 'abcdefg'
        m.int2 = 12345
        m.str2 = 'gfedcba' 
        m.int3 = 123456789
        m.int4 = 123456789234234234
        m.array1 = [3,2,1]
        return m
    
    
    def testSimpleSerialization(self):
        m = self.createTestMessage()
        serialized = StringIO(Serializer.serialize(m))
        
        deserialized = Serializer.deserialize(serialized, TestMessage1)
        
        self.assertDictEqual(m.__dict__, deserialized.__dict__)
        
    
if __name__ == '__main__':
    unittest.main()