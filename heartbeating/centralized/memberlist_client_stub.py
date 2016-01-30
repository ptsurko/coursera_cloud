from heartbeating.messages import JoinRequestMessage, JoinResponseMessage, MemberlistRequestMessage
from proto.rpc.client import RpcClientStub, client, method
from proto.rpc.messages import EmptyResponseMessage

@client()
class MemberlistClientStub(RpcClientStub):
    
    @method(MemberlistRequestMessage, EmptyResponseMessage)
    def update(self, message):
        pass
    
    @method(JoinRequestMessage, JoinResponseMessage)
    def join(self, message):
        pass