
import abc
import threading

class BaseModule(object):
    def __init__(self, options={}):
        self.options = options

    @abc.abstractmethod
    def attach(self, server):
        pass
    
    @abc.abstractmethod
    def detach(self, server):
        pass
    

class BaseThreadedModule(BaseModule):
    def attach(self, server):
        self._stopped = threading.Event()
        self._thread = threading.Thread(target=self.run, args=(server,))
        self._thread.start()
    
    @abc.abstractmethod
    def run(self, server):
        pass
    
    def detach(self, server):
        self._stopped.set()
        # TODO: add timeout
        self._thread.join()
        
    def is_stopped(self):
        return self._stopped.is_set()
    
    def wait(self, timeout):
        self._stopped.wait(timeout)