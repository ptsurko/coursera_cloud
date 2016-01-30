from proto.message import Message
from proto.field_type import FieldType
from proto.serializable import serializable, field
from proto.rpc.messages import RequestMessage, ResponseMessage

@serializable()
@field('host', FieldType.String)
@field('port', FieldType.Int16)
class AddressMessage(Message):
    def __init__(self, host='', port=0):
        self.host = host
        self.port = port

@serializable()
@field('address', FieldType.Object, object_class=AddressMessage)
@field('seq_num', FieldType.Int32)
class HeartbeatRequestMessage(RequestMessage):
    def __init__(self, address=None, seq_num=0):
        self.address = address
        self.seq_num = seq_num
        

@serializable()
@field('address', FieldType.Object, object_class=AddressMessage)
class JoinRequestMessage(RequestMessage):
    def __init__(self, address=None):
        self.address = address
        
        
@serializable()
@field('central_address', FieldType.Object)
class JoinResponseMessage(ResponseMessage):
    def __init__(self, central_address=None):
        self.central_address = central_address
        
        
@serializable()
@field('host', FieldType.String)
@field('port', FieldType.Int16)
@field('seq_num', FieldType.Int32)
class MemberMessage(Message):
    def __init__(self, host='', port=0, seq_num=0):
        self.host = host
        self.port = port
        self.seq_num = seq_num


@serializable()
@field('members', FieldType.List, list_item_class=MemberMessage)
class MemberlistRequestMessage(RequestMessage):
    def __init__(self, members=[]):
        self.members = members