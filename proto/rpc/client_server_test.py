# # 
# # @rpc.client()
# # class PingClientStub(RPCClient):
# #     
# #     @rpc.method(PingMessageRequest, PingMessageResponse)
# #     def ping(self, ping_message):
# #         pass
# #     
# # @rpc.server()    
# # class PingServer(RPCServer):
# #     
# #     @rpc.handler(PingMessageRequest, PingMessageResponse)
# #     def ping(self, ping_message):
# #         
# #         return pong_message
# # 
# # 
# # channel = RPCChannel(host, port)
# # client = RPCClient(channel)
# # client.ping(ping_message)
# # 
# # 
# # server = RPCServer(port)
# # server.Loop()
# 
# import threading
# import time
# 
# from proto.message_descriptor import MessageDescriptor
# from proto.field_descriptor import FieldDescriptor
# from proto.field_type import FieldType
# from proto.message import Message
# from proto.serializable import serializable
# 
# from proto.rpc._method_descriptor import _MethodDescriptor
# from proto.rpc.server.rpcserver import RpcServer, service, handler
# from proto.rpc.client.rpcchannel import RpcChannel
# from proto.rpc.service.rpcservice_stub import RpcServiceStub
# 
# class TestMessageDescriptor(MessageDescriptor):
#     def __init__(self):
#         super(self.__class__, self).__init__('TestMessage', fields=[
#             FieldDescriptor('int1', FieldType.Int8)
#         ])
# 
# @serializable(TestMessageDescriptor())
# class TestMessage(Message):
#     def __init__(self, int1=0):
#         self.int1 = int1
# 
# @service()
# class TestRpcService(RpcServiceStub):
#     
#     @handler(TestMessage, None)
#     def TestMethod(self):
#         pass
#     
#     def Dispatch(self, method_descriptor, message):
#         print '%r' % message.int1
#         
#         self.Shutdown()
# 
# def start_server():
#     server = TestRPCServer(port=8081, service=)
#     server.loop()
# 
# server_thread = threading.Thread(target=start_server)
# server_thread.start()
# 
# time.sleep(5)
# 
# message = TestMessage(10)
# channel = RPCChannel('localhost', 8081)
# channel.call_method(_MethodDescriptor('TestMethod', message.__class__), message)
# 
# server_thread.join()
