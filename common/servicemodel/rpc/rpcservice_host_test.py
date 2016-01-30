import threading
import time
import unittest
from rpcservice_host import RpcSericeHost

from common.address import Address
from common.servicemodel.rpc.client_stub import RpcClientStub
from common.servicemodel.rpc.service_stub import RpcServiceStub
from common.servicemodel.rpc.contract_attributes import handler, service, client, method
from proto.message import Message
from proto.serializable import serializable

@serializable()
class TestMessage(Message):
    pass

@client()
class TestClientStub(RpcClientStub):
    @method(TestMessage)
    def method(self, message):
        pass

@service()
class TestServiceStub(RpcServiceStub):
    def __init__(self, event):
        self._event = event
        
    @handler(TestMessage)
    def method(self, message):
        self._event.set()

class MemberlistManagerTest(unittest.TestCase):
    def setUp(self):
        pass
    
    def testServiceMethod(self):
        address = Address('localhost', 8085)
        event = threading.Event()
        service_stub = TestServiceStub(event)
        
        service_host = RpcSericeHost(service_stub, address)
        thread = self._runServiceInThread(service_host)
        while not thread.isAlive():
            time.sleep(0.01)
        
        
        client_stub = TestClientStub(address)
        client_stub.method(TestMessage())
        
        event.wait(20)
        service_host.shutdown(True)
        self.assertTrue(event.is_set())
    
    def _runServiceInThread(self, service_host):
        thread = threading.Thread(target=service_host.loop)
        thread.start()
        return thread
     

if __name__ == '__main__':
    unittest.main()
    