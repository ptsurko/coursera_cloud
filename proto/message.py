from serializer import Serializer

class Message(object):
    _descriptor = None
    
    @classmethod
    def get_descriptor(cls):
        return cls._descriptor
    
    def serialize_to_string(self):
        serializer = Serializer()
        return serializer.serialize(self)
    
    def parse_from_string(self, serialized):
        serializer = Serializer()
        return serializer.deserialize(serialized, self.__class__)
    
    def repr(self):
        return 