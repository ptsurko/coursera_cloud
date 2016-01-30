
from proto import FieldType, Message, serializable, field

@serializable()
@field('message', FieldType.String)
class ErrorMessage(Message):
    def __init__(self, message=''):
        self.message = message
        
    def repr(self):
        return '%s(%s)' % (self.__class__.__name__, self.message)