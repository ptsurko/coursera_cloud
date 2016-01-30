
import socket

class BaseChannel(object):
    def __init__(self, address, timeout=None):
        self.address = address
        self.sock = None
        self.timeout = timeout
        
    def connect(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.settimeout(self.timeout)
        self.sock.connect((self.address.host, self.address.port))
        
    
    def send(self, data):
        self.sock.sendall(data)
        
    def receive(self, recv_size=4096):
        received_data = ''
        while True:
            data = self.sock.recv(recv_size)
            received_data += data
            if len(data) < recv_size:
                break
        
        return received_data
    
    def close(self):
        if self.sock:
            self.sock.close()
            self.sock = None