

class _MessageDescriptor(object):
    def __init__(self, name=None, fields = None):
        self.name = name
        self.fields = fields if fields else []