import os
import random
import signal
import threading
import time

class ServiceFailureMixin(object):
    def start_failure_generator(self):
        thread = threading.Thread(target=self._failure_thread_worker)
        thread.start()
        
    def _failure_thread_worker(self):
        while True:
            time.sleep(5);
            
            if random.randint(0, 10) < 6:
                print 'aborting process %d' % os.getpid()
#                 os.abort()
                os.kill(os.getpid(), signal.SIGTERM)
                
                signal.SIGTERM
                
                return
            
                
            