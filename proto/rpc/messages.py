from proto.message import Message
from proto.serializable import serializable

class RequestMessage(Message):
    pass

class ResponseMessage(Message):
    pass

@serializable()
class EmptyResponseMessage(ResponseMessage):
    pass