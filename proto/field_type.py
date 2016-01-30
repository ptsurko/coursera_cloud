
from enum import IntEnum

# Negative numbers. See ZigZag in protobuf
# Float/Double



class FieldType(IntEnum):
    Int8 = 1
    Int16 = 2
    Int32 = 4
    Int64 = 8
    String = 16
    List = 32
    Object = 64
    
#     Bool = 1
#     Int = 1
#     Long = 2
#     Enum = 11
#     String = 16
#     List = 32
#     Object = 64
    