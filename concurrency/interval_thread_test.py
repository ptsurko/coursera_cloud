
import threading
import unittest

from concurrency.interval_thread import IntervalThread

class IntervalThreadTest(unittest.TestCase):
    
    def testWorkAsArgument(self):
        event = threading.Event()
        def func():
            event.set()
        thread = IntervalThread(callback=func)
        thread.start()
        event.wait(1)
        thread.stop()
        
        assert event.is_set() == True

if __name__ == '__main__':
    unittest.main()
    