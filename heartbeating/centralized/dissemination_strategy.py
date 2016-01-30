
from common.member import MemberStatus

class DisseminationStrategy(object):
    def __init__(self, disseminator):
        self._disseminator = disseminator
        
    def disseminate(self, memberlist):
        endpoint_addreses = []
        with memberlist.lock():
            for member in memberlist.itervalues():
                if member.status != MemberStatus.Dead:
                    endpoint_addreses.append(member.address)
                
        for address in endpoint_addreses:
            self._disseminator.send(memberlist, address)
        