import logging

from proto.rpc.service.rpcservice_stub import RpcServiceStub, handler, service
from common.member import Member
from heartbeating.messages import MemberlistRequestMessage, JoinRequestMessage, JoinResponseMessage, AddressMessage
from proto.rpc.messages import EmptyResponseMessage
from proto.rpc.server.baseserver import ServerException

@service()
class MemberlistServiceStub(RpcServiceStub):
    def __init__(self, memberlist, service, options, logger=logging.getLogger('MemberlistService')):
        self._memberlist = memberlist
        self._logger = logger
        self._options = options
        self._service = service
        
    @handler(MemberlistRequestMessage, EmptyResponseMessage)
    def update(self, message):
        with self._memberlist.lock():
            self._merge_message_into_memberlist(message, self._memberlist)

        self._logger.debug('Updated memberlist.')
        
        return EmptyResponseMessage()
        
    def _merge_message_into_memberlist(self, message, memberlist):
        for new_member in message.members:
            new_key = memberlist.generate_key(new_member.host, new_member.port)
            
            for existing_key, existing_member in memberlist.iteritems():
                if existing_key == new_key:
                    existing_member.seq_num = new_member.seq_num
                    break
            else:
                member = Member(AddressMessage(host=new_member.host, port=new_member.port), new_member.seq_num)
                memberlist.set(new_key, member)
                
    @handler(JoinRequestMessage, JoinResponseMessage)
    def join(self, message):
        if self._options.is_controller:
            address = self._service.options.address
            central_address = AddressMessage(address.host, address.port)
        elif self._options.controller:
            central_address = AddressMessage(self._options.controller.host, self._options.controller.port)
#         else:
#             raise ServerException('Controller hasn\'t been set.')
        
        return JoinResponseMessage(central_address)