
import unittest
from promise import Promise, PromiseException

class PromiseTest(unittest.TestCase):
    def setUp(self):
        self.promise = Promise()
    
    def testOnFulfilledCallback(self): # 2.2.2.1
        self.called_ = False
        def resolveCallback(val):
            self.called_ = True
            self.assertEqual(10, val)
            
        self.promise.then(resolveCallback)
        self.promise.resolve(10)
        
    def testResolveCannotBeCalledTwice(self): # 2.2.2.2/2.2.2.3
        self.promise.resolve(10)
        with self.assertRaises(PromiseException):
            self.promise.resolve(10)
        
    def testOnRejectedCallback(self): # 2.2.3.1
        self.called_ = False
        def rejectCallback(error):
            self.called_ = True
            self.assertIsInstance(error, Exception)
            
        self.promise.then(lambda _: _, rejectCallback)
        self.promise.reject(Exception('test'))
    
    
    def testRejectCannotBeCalledTwice(self): # 2.2.3.2/2.2.3.3
        self.promise.reject(Exception('test'))
        with self.assertRaises(PromiseException):
            self.promise.reject(Exception('test'))
            
            
    def testFulfilledCallbacksOrder(self): # 2.2.6.1
        self.index = 0
        def callback1():
            self.index += 1
            self.assertEqual(self.index, 1)
            
        def callback2():
            self.index += 1
            self.assertEqual(self.index, 2)
            
        self.promise.resolve(10)
        
    def testRejectedCallbacksOrder(self): # 2.2.6.2
        pass
    
    
    
    
    
if __name__ == '__main__':
    unittest.main()