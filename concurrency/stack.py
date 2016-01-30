# import threading
# 
# # TODO: add timeouts
# 
# class Empty(Exception):
#     "Exception raised by Stack.get(block=0)/get_nowait()."
#     pass
# 
# class Stack(object):
#     def __init__(self, size=None):
#         self._lock = threading.Lock()
#         self._head = _Node(None)
#         self._tail = self._head;
# 
#     def put(self, item):
#         with self._lock:
#             self._tail = _Node(item, self._head)
#         
#     def get(self):
#         with self._lock:
#             if self._head == self._tail:
#                 raise Empty()
#             
#             result = self._tail.value
#             self._tail = self._tail.prev
#             return result
# 
#     
# class _Node(object):
#     def __init__(self, value, prev=None):
#         self.value = value;
#         self.prev = prev;
#         
