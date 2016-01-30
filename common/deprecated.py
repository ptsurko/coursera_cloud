import functools
import warnings

def deprecated(func):
    @functools.wraps(func)
    def new_func(*args, **kwargs):
        warnings.warn("Function %s deprecated." % func.__name__, DeprecationWarning)
        
        return func(*args, **kwargs)
        
    return new_func