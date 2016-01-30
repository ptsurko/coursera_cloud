
from proto.field_type import FieldType

class _FieldDescriptor(object):
    def __init__(self, name, field_type, list_item_type=FieldType.Object, list_item_class=None, object_class=None, enum_class=None):
        self.name = name
        self.type = field_type
        self.list_item_type = list_item_type
        self.list_item_class = list_item_class
        self.enum_class = enum_class
        self.object_class = object_class