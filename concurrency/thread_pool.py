
import functools
import threading
import time

from concurrency.queue import Queue, EmptyException

class ThreadPool(object):
    def __init__(self, num_workers=None, max_workers=None):
        self._threads = []
        self._queue = Queue()
        
        for _ in range(num_workers):
            self._threads.append(_PoolThread(self._queue))

    def execute(self, func, *args, **kwargs):
        self._queue.put(functools.partial(func, *args, **kwargs))
    
    def stop(self):
        for t in self._threads:
            t.stop()
    

class _PoolThread(threading.Thread):
    def __init__(self, queue):
        super(self.__class__, self).__init__()
        self._stopped = threading.Event()
        self._queue = queue
        pass

    def run(self):
        while not self._stopped.isSet():
            try:
                func = self._queue.get()
                func()
            except EmptyException:
                time.sleep(1)
            

    def stop(self):
        self._stopped.set()