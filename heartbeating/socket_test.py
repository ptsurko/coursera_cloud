# 
# import multiprocessing
# import socket
# import time
# 
# server_address = ('localhost', 10239)
# 
# class Sender(multiprocessing.Process):
#     def __init__(self, id):
#         super(Sender, self).__init__()
#         self.id = id
#         
#     def run(self):
#         sock = None
#         try:
#             sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# #             sock.settimeout(3)
#             sock.connect(server_address)
#             sock.send('message %d' % self.id)
#         except Exception as e:
#             print 'Exception for %d: %s' % (self.id, e)
#         finally:
#             sock.close()
#     
# class Receiver(multiprocessing.Process):
#     
#     def run(self):
#         sock = None
#         try:
#             sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#             sock.bind(server_address)
#             sock.listen(1)
#             
#             while True:
#                 conn, _ = sock.accept()
#                 
#                 process = multiprocessing.Process(target=self._handle_connection, args=(conn,))
#                 process.start()
#                 
#         finally:
#             sock.close()
# 
#     def _handle_connection(self, conn):
#         try:
#             message = ''
#             while True:
#                 data = conn.recv(16)
#                 message += data
#                         
#                 if len(data) < 16:
#                     break
#         except Exception as e:
#             print 'Exception: %s' % e
#         finally:
#             conn.close()
#         print 'message: %s' % message
#         time.sleep(5)
# 
# receiver = Receiver()
# senders = [Sender(i) for i in range(7)]
# 
# receiver.start()
# for sender in senders:
#     sender.start()
# 
# receiver.join()
# for sender in senders:
#     sender.join()