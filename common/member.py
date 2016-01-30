
from enum import Enum

class MemberStatus(Enum):
    Undefined = 0
    Alive = 1
    Suspected = 2
    Dead = 4

class Member(object):
    def __init__(self, address, seq_num=0, timestamp=0, status=MemberStatus.Alive):
        self.address = address
        self.seq_num = seq_num
        self.timestamp = timestamp
        self.status = status
    
    def merge(self, node):
        if self.address != node.address:
            raise Exception()

        if self.timestamp < node.timestamp:
            self.seq_num = node.seq_num
            self.timestamp = node.timestamp
            self.status = node.status

    def __repr__(self):
        return '%s(%s, %s, %s)' % (self.__class__.__name__, self.address, self.seq_num, self.timestamp)
    
    def __str__(self):
        return '%s(%r)' % (self.__class__.__name__, self.__dict__)
    
# class Member2(object):
#     pass