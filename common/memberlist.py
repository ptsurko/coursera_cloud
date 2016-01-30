
import collections
import contextlib
import threading

#TODO: add lock for memberlist
class MemberList(collections.MutableMapping):
    def __init__(self, *args, **kwargs):
        self.store = dict()
        self.update(dict(*args, **kwargs))  # use the free update to set keys
        self._lock = threading.Lock()

    def __getitem__(self, key):
        return self.store[key]

    def __setitem__(self, key, value):
        self.store[key] = value

    def __delitem__(self, key):
        del self.store[key]

    def __iter__(self):
        return iter(self.store)

    def __len__(self):
        return len(self.store)
    
    def __str__(self):
        return "MemberList:[\n%s]" % ",\n".join(map(lambda endpoint: str(endpoint), self.itervalues()))
    
    @contextlib.contextmanager
    def lock(self):
        self._lock.acquire()
        yield self
        self.unlock()
        
    
    def unlock(self):
        self._lock.release()
    
    def set(self, key, endpoint):
        self[key] = endpoint
    
    def merge(self, memberlist):
        for key1, endpoint1 in memberlist.iteritems():
            for key2, endpoint2 in self.iteritems():
                if key1 == key2:
                    endpoint2.merge(endpoint1)
                    break
            else:
                self.set(key1, endpoint1)
                
    def generate_key(self, host, port):
        return '%s:%s' % (host, port)
                       
                
# class Memberlist2(object):
#     def __init__(self):
#         self._members = []
#         self._lock = threading.Lock()
#     
#     def __len__(self):
#         pass
#     
#     def __getitem__(self, key):
#         for member in self._members:
#             if member.
#     
#     def __iter__(self):
#         return self._members
#     
#     def lock(self):
#         self._lock.acquire()
#     
#     def unlock(self):
#         self._lock.release()
#     
#     def clone(self):
#         pass
        