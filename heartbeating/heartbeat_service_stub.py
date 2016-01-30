import logging

from common.address import Address
from proto.rpc.service import RpcServiceStub, handler, service
from common.member import Member
from common.timestamp import timestamp
from heartbeating.messages import HeartbeatRequestMessage

@service()
class HeartbeatServiceStub(RpcServiceStub):
    def __init__(self, memberlist, logger=logging.getLogger('HeartbeatService')):
        self._memberlist = memberlist
        self._logger = logger
    
    @handler(HeartbeatRequestMessage)
    def beat(self, message):
        with self._memberlist.lock():
            address = message.address
            memberlist_key = self._memberlist.generate_key(address.host, address.port)
            
            # TODO: add locking for memberlist
            node = Member(Address(address.host, address.port), message.seq_num, timestamp())
            
            if memberlist_key in self._memberlist:
                self._memberlist[memberlist_key].merge(node)
            else:
                self._memberlist[memberlist_key] = node
        
        self._logger.debug('Received heartbeat message %s from %s.' % (message.seq_num, node.address))