import logging
import threading
import time


class IntervalThread(threading.Thread):
    def __init__(self, callback=None, interval=0, continue_on_erro=True, logger=logging.getLogger('IntervalThread'), args=(), kwargs={}):
        self._interval = interval
        self._stopped = threading.Event()
        self._callback = callback
        self._args = args
        self._kwargs = kwargs
        self._continue_on_error = continue_on_erro
        self._logger = logger
        
        threading.Thread.__init__(self)
        
        
    def run(self):
        while not self._stopped.is_set():
            time.sleep(self._interval)
            try:
                self.work()
            except Exception as e:
                self._logger.error(e)
                
                raise
            
                if self._continue_on_error:
                    continue
                else:
                    raise
    
    def work(self):
        if self._callback != None:
            self._callback(*self._args, **self._kwargs)
    
    def stop(self):
        self._stopped.set()