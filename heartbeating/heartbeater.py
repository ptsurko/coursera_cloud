import logging

from heartbeating.messages import HeartbeatRequestMessage, AddressMessage
from heartbeating.heartbeat_client_stub import HeartbeatClientStub

class Heartbeater(object):
    def __init__(self, address, logger=logging.getLogger('Heartbeater')):
        self._seq_num = 0
        self._address = address
        self._logger = logger
    
    def heartbeat(self, controller_address):
        self._seq_num += 1
        
        message = HeartbeatRequestMessage()
        message.seq_num = self._seq_num
        message.address = AddressMessage(self._address.host, self._address.port)
        
        self._logger.debug('Sending heartbeat message  %s to service %s.' % (message.seq_num, controller_address))
        
        self._heartbeat_client = HeartbeatClientStub(controller_address)
        self._heartbeat_client.beat(message)