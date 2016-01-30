
class _ServiceDescriptor(object):
    def __init__(self, name, methods=[]):
        self.name = name
        self._methods = methods
    
    def get_method(self, method_name):
        for method in self._methods:
            if method.name == method_name:
                return method
        
        raise Exception('')
    
    def add_method(self, method):
        self._methods.append(method)