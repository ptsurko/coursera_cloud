import logging

from common.member import MemberStatus
from common.timestamp import timestamp

class FaultDetector(object):
    def __init__(self, suspiction_timeout=5, dead_timeout=5, cleanup_timeout=15, logger=logging.getLogger('FaultDetector')):
        self._suspiction_timeout = suspiction_timeout
        self._dead_timeout = dead_timeout
        self._cleanup_timeout = cleanup_timeout
        self._logger = logger
    
    def suspect(self, address):
        pass
#         memberlist[address].status = MemberStatus.Suspected
    
    def detect(self, memberlist):
        self._logger.debug('Detecting failures.')
        dead_nodes = []
        current_timestamp = timestamp()
        for node in memberlist.itervalues():
            if node.timestamp + self._dead_timeout * 1000 < current_timestamp:
                print 'failed node: %r' % node 
                node.status = MemberStatus.Dead
                dead_nodes.append(node)
        
        # self._logger.debug('Detecting failures.')
        return dead_nodes