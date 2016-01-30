
class _MethodDescriptor(object):
    def __init__(self, name, method, request_class, response_class=None):
        self.name = name
        self.method = method
        self.request_class = request_class
        self.response_class = response_class