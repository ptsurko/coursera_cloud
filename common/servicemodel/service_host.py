
import errno
import logging
import socket
import sys
import threading

class SericeOptions(object):
    pass
#     def __init__(self, address=None):
#         self.address = address

class ServiceHost(object):
    def __init__(self, address, options=None, logger=logging.getLogger('Server')):
        #TODO: pass address as string
        self.address = address
        self.logger = logger
        
        self.options = options if options else SericeOptions()
        
        self._shutdown_flag = False
        self._shutdown_event = threading.Event()
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._sock.settimeout(1)
        #TODO: timeout for connection
        
        
#         self._modules = []
#         self._handlers = []
        
#     def add_module(self, module):
#         self._modules.append(module)
    
#     def add_handler(self, handler):
#         self._handlers.append(handler)
    
    def loop(self):
#         self._attach_modules()
        address = self.address
        try:
            self._sock.bind((address.host, address.port))
            self._sock.listen(5)
            
            while not self._shutdown_flag:
                try:
                    conn = self._get_connection()
                except socket.timeout:
                    continue
                
                except socket.error as (code, _):
                    if code == errno.EINTR:
                        break
                    raise
                
                self.handle_connection(conn)
        except Exception as e:
            print 'exception: %s' % e
        finally:
#             self._sock.shutdown(socket.SHUT_RDWR)
            print 'closing server socket'
#             self._sock.shutdown(1)
            self._sock.close()
            
#             self._sock.close()
            
            self._shutdown_event.set()
#             self._detach_modules()
            
#     def _attach_modules(self):
#         for m in self._modules:
#             try:
#                 m.attach(self)
#             except Exception as e:
#                 self.logger.error(e, exc_info=sys.exc_info())
#                 raise
# 
#     def _detach_modules(self):
#         for m in self._modules:
#             try:
#                 m.detach(self)
#             except Exception as e:
#                 self.logger.error(e, exc_info=sys.exc_info())
#                 raise

    def handle_connection(self, conn):
        try:
            address = conn.address
            data = self._read(conn.socket)
            
            try:
                response = self.process_request(address, data)
            except Exception as e:
                response = self.handle_error(address, e, sys.exc_info())
            
            # TODO: don't write to socket if communication is one-way
            if response is not None:
                self._write(conn.socket, response)

        # TODO: handle socket errors
        except Exception as e:
            print 'server: connection exception: %s' % e
            self.logger.error(e, exc_info=sys.exc_info())
            raise e
        finally:
            print 'server: closing client socket.'
            conn.close()

    def process_request(self, address, data):
        for h in self._handlers:
            if h.can_handle(data):
                return h.handle(data)
        else:
            raise ServerException('Unable to process request.')

    def handle_error(self, address, exception, exc_info):
        return exception.message

    def shutdown(self, wait=False):
        self._shutdown_flag = True
        if wait:
            self._shutdown_event.wait(20)
                    
    def _get_connection(self):
        socket, address = self._sock.accept()
        return _Connection(socket, address)

    def _read(self, socket, recv_size=4096):
        received_data = ''
        while True:
            data = socket.recv(recv_size)
            received_data += data
            if len(data) < recv_size:
                break
        
        return received_data

    def _write(self, socket, data):
        socket.sendall(data)

class _Connection(object):
    def __init__(self, socket, address):
        self.socket = socket
        self.address = address
    
    
    def close(self):
        try:
            self.socket.shutdown(socket.SHUT_WR)
        except:
            pass
        self.socket.close()
        
class ServerException(Exception):
    pass