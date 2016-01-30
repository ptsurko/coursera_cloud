from proto.rpc.client.rpcclient_stub import RpcClientStub, method, client
from heartbeating.messages import HeartbeatRequestMessage

@client()
class HeartbeatClientStub(RpcClientStub):
    
    @method(HeartbeatRequestMessage)
    def beat(self, message):
        pass
        