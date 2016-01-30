
import unittest

from concurrency.queue import Queue, Empty

class QueueTestCase(unittest.TestCase):
    def setUp(self):
        self.queue = Queue()
        
    def testSetGet(self):
        
        self.queue.put(1)
        self.queue.put(2)
        self.queue.put(3)
        
        self.assertEqual(self.queue.get(), 1)
        self.assertEqual(self.queue.get(), 2)
        self.assertEqual(self.queue.get(), 3)
    
    def testSetGet2(self):
        
        self.queue.put(1)
        self.assertEqual(self.queue.get(), 1)
        
        self.queue.put(2)
        self.assertEqual(self.queue.get(), 2)
    
    def testEmpty(self):
        self.assertRaises(Empty, self.queue.get)

if __name__ == '__main__':
    unittest.main()