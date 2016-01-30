import threading

# TODO: add timeouts

class EmptyException(Exception):
    "Exception raised by Queue.get(block=0)/get_nowait()."
    pass

class Queue(object):
    def __init__(self, size=None):
        self._lock = threading.Lock()
        self._head = None
        self._tail = None

    def put(self, item):
        with self._lock:
            if self._head == None:
                self._head = self._tail = _Node(item)
            else:
                self._tail.next = _Node(item)
                self._tail = self._tail.next
            
        
    def get(self, timeout=None):
        with self._lock:
            if self._head == None:
                raise EmptyException()
            
            result = self._head.value
            
            if self._head == self._tail:
                self._tail = None
            
            self._head = self._head.next
            return result

    
class _Node(object):
    def __init__(self, value):
        self.value = value;
        self.next = None;
        
