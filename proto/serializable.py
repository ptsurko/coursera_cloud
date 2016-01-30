from proto.serializer import Serializer
from proto.field_type import FieldType
from proto._message_descriptor import _MessageDescriptor
from proto._field_descriptor import _FieldDescriptor

def serializable2(descriptor):
    def func(class_obj):
        class_obj._descriptor = descriptor
        Serializer.register_message_descriptor(class_obj, class_obj._descriptor)
        
        return class_obj
    return func

def serializable(name=None):
    def func(class_obj):
        if class_obj._descriptor:
            class_obj._descriptor.name = name if name else class_obj.__name__
        else:
            class_obj._descriptor = _MessageDescriptor(name if name else class_obj.__name__)
            Serializer.register_message_descriptor(class_obj, class_obj._descriptor)
        
        return class_obj
    return func


def field(name, field_type, list_item_type=FieldType.Object, list_item_class=None, object_class=None, enum_class=None):
    def func(class_obj):
        if class_obj._descriptor is None:
            class_obj._descriptor = _MessageDescriptor()
            Serializer.register_message_descriptor(class_obj, class_obj._descriptor)
            
        field = _FieldDescriptor(name, field_type=field_type, list_item_type=list_item_type, list_item_class=list_item_class, object_class=object_class, enum_class=enum_class)
        class_obj._descriptor.fields.append(field)
        return class_obj
    return func