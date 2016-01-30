import logging
import time

from common.process import ServerProcess
from common.misc.service_failure_mixin import ServiceFailureMixin

from heartbeating.centralized.memberlist_client_stub import MemberlistClientStub
from heartbeating.centralized.modules import MemberlistOptions, Memberlist
from common.address import Address
from heartbeating.messages import JoinRequestMessage, AddressMessage

logging.basicConfig(format='%(asctime)s - %(process)d - %(name)s - %(levelname)s - %(module)s:%(message)s', datefmt='%H:%M:%S', level=logging.DEBUG)
    
class ControllerProcess(ServerProcess):
    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(name='Central Service', *args, **kwargs)
        
        memberlist_options = MemberlistOptions(is_controller=True)
        self.rpc_server.add_module(Memberlist(options=memberlist_options))
    
    def join_group(self, controller_address):
        pass

class WorkerProcess(ServerProcess, ServiceFailureMixin):
    def __init__(self, controller_address, *args, **kwargs):
        super(self.__class__, self).__init__(name='Worker Service', *args, **kwargs)

        memberlist_options = MemberlistOptions(controller_address=controller_address)
        self.rpc_server.add_module(Memberlist(options=memberlist_options))
    
    def run(self):
        self.start_failure_generator()
        
        ServerProcess.run(self)
        
    def join_group(self, controller_address):
        client = MemberlistClientStub(controller_address, timeout=5)
        address = AddressMessage('localhost', 0)
        request = JoinRequestMessage(address)
        client.join(request)
        

def main():
    controller_port = 10011
    services = []
    controller_address = Address('localhost', controller_port)
    
    controller_service = ControllerProcess(port=controller_port)
    services.append(controller_service)
    for i in range(1):
#         config = WorkerConfig(controller_address=Address('localhost', controller_port))
        service = WorkerProcess(port=controller_port + i + 1, controller_address=controller_address)
        services.append(service)
    
    for service in services:
        service.start()
    
    time.sleep(5)
    for service in services:
        service.join_group(controller_address)
    
    for service in services:
        service.join()


if __name__ == '__main__':
    main()
    