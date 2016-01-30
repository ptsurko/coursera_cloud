import logging

from heartbeating.centralized.memberlist_client_stub import MemberlistClientStub
from heartbeating.messages import MemberlistRequestMessage, MemberMessage

class MemberlistDisseminator(object):
    def __init__(self, fault_detector, logger=logging.getLogger('MemberlistDisseminator')):
        self._logger = logger
        self._fault_detector = fault_detector
    
    def send(self, memberlist, address):
        
        message = MemberlistRequestMessage()
        
        with memberlist.lock():
            for member in memberlist.itervalues():
                member_message = MemberMessage(member.address.host, member.address.port, member.seq_num)
                message.members.append(member_message)
        
        self._logger.debug('Sending MemberlistMessage to %s.' % (address,))
        
        try:
            client = MemberlistClientStub(address, timeout=5)
            client.update(message)
        except Exception as e:
            self._logger.error('Unable to send memberlist \'%s\'.' % e.message, exc_info=True)

            self._fault_detector.suspect(address)
