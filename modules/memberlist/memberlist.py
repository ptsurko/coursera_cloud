import copy
import threading

class Memberlist(object):
    _lock = threading.Lock()
    
    def __init__(self, members=None):
        self._members = members if members is not None else []
        
    def __len__(self):
        return len(self._members)
    
    def __iter__(self):
        return iter(self._members)
    
    def __getitem__(self, key):
        if isinstance(key, int):
            if key < 0 or key > len(self._members):
                raise KeyError()
            return self._members[key]
        else:
            raise TypeError()
    
    def get_by_address(self, address):
        for member in self._members:
            if member.address == address:
                return member
        
        raise MemberlistException("Could not find '%s' in memberlist." % address)
    
    def __repr__(self):
        pass
    
    def __copy__(self):
        return Memberlist([copy.copy(member) for member in self._members])
    
class MemberlistException(Exception):
    pass