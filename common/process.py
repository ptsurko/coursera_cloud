
import logging
import multiprocessing
import signal
from proto.rpc.server import RpcServer
from proto.rpc.server.baseserver import ServerOptions
from common.address import Address

# IMPROVEMENTS:
#  - Try ProtoBuf for message serializing

class ServerConfig(object):
            
    def __str__(self):
        return '%r' % self.__dict__


class ServerProcess(multiprocessing.Process):
    def __init__(self, host='localhost', port=8080, config=ServerConfig(), name='Service'):
        super(ServerProcess, self).__init__()

        self.name = name
        self.config = config
        self.logger = logging.getLogger(self.name)
        
        server_options = ServerOptions(address=Address(host=host, port=port))
        self.rpc_server = RpcServer(options=server_options, logger=self.logger)
        
    def _sign_handler(self, signal, frame):
        self.rpc_server.shutdown()
    
    def run(self):
        self.logger.info('Starting %s.' % self.name)
        self.logger.debug('Service configuration %s.' % self.config)
        
        signal.signal(signal.SIGTERM, self._sign_handler)
        signal.signal(signal.SIGINT, self._sign_handler)
        
        self.rpc_server.loop()
        
        self.logger.info('Terminating %s.' % self.name)