import errno
import logging
import socket
import sys
import threading

class ServerOptions(object):
    def __init__(self, address=None):
        self.address = address

class BaseServer(object):
    def __init__(self, options=ServerOptions(), logger=logging.getLogger('Server')):
        self.options = options
        self.logger = logger
        
        self._shutdown_flag = threading.Event()
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #TODO: timeout for connection
        
        
        self._modules = []
        self._handlers = []
        
    def add_module(self, module):
        self._modules.append(module)
    
    def add_handler(self, handler):
        self._handlers.append(handler)
    
    def loop(self):
        self._attach_modules()
        address = self.options.address
        try:
            self._sock.bind((address.host, address.port))
            self._sock.listen(5)
            
            while not self._shutdown_flag.is_set():
                try:
                    conn = self._get_connection()
                except socket.timeout:
                    continue
                
                except socket.error as (code, _):
                    if code == errno.EINTR:
                        break
                    raise
                
                self.handle_connection(conn)
#         except Exception e:
#             print 'exception: port %d in use.' % self.options.port
        finally:
            self._sock.close()
            self._detach_modules()
            
    def _attach_modules(self):
        for m in self._modules:
            try:
                m.attach(self)
            except Exception as e:
                self.logger.error(e, exc_info=sys.exc_info())
                raise

    def _detach_modules(self):
        for m in self._modules:
            try:
                m.detach(self)
            except Exception as e:
                self.logger.error(e, exc_info=sys.exc_info())
                raise

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
            self.logger.error(e, exc_info=sys.exc_info())
            raise e
        finally:
            conn.close()

    def process_request(self, address, data):
        for h in self._handlers:
            if h.can_handle(data):
                return h.handle(data)
        else:
            raise ServerException('Unable to process request.')

    def handle_error(self, address, exception, exc_info):
        return exception.message

    def shutdown(self):
        self._shutdown_flag.set()
                    
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
        
