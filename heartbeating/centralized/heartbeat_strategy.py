from heartbeating.heartbeat_strategy import HeartbeatStrategy

class CentralizedHeartbeatStrategy(HeartbeatStrategy):
    def __init__(self, heartbeater, controller_address):
        self._heartbeater = heartbeater
        self._controller_address = controller_address
    
    def heartbeat(self):
        self._heartbeater.heartbeat(self._controller_address)