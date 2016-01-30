
from enum import IntEnum

class MemberState(IntEnum):
    Undefined = 0
    New = 1
    Alive = 2
    Suspected = 4
    Dead = 8 

class Member(object):
    def __init__(self, address, seq_num, timestamp, state=MemberState.Undefined):
        self._address = address
        self._seq_num = seq_num
        self._state = state
        self._timestamp = timestamp
        
    @property
    def address(self):
        return self._address
    
    @property
    def seq_num(self):
        return self._seq_num
    
    @property
    def state(self):
        return self._state
    
    @property
    def timestamp(self):
        return self._timestamp
    
    def __copy__(self):
        return Member(self._address, self._seq_num, self._timestamp, self._state)
    
    #TODO: check if i need this
    def __deepcopy__(self):
        pass
    
    def __repr__(self):
        return "%s(%s, %s, %s, %s)" % (self.__class__.__name, self._address, self._seq_num, self._timestamp, self._state)