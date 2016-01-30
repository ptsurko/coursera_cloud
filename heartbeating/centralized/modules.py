from concurrency.interval_thread import IntervalThread
from proto.rpc.server.modules import BaseModule
from heartbeating.heartbeater import Heartbeater
from common.memberlist import MemberList
from common.fault_detector import FaultDetector
from heartbeating.heartbeat_service_stub import HeartbeatServiceStub
from heartbeating.centralized.memberlist_disseminator import MemberlistDisseminator
from heartbeating.centralized.heartbeat_strategy import CentralizedHeartbeatStrategy
from heartbeating.centralized.dissemination_strategy import DisseminationStrategy
from heartbeating.centralized.memberlist_service_stub import MemberlistServiceStub

class MemberlistOptions(object):
    def __init__(self, is_controller=False, controller_address=None, heartbeat_interval=3, dissemination_interval=3, fault_detection_interval=3):
        self.is_controller = is_controller
        self.controller_address = controller_address
        self.fault_detection_interval = fault_detection_interval
        self.heartbeat_interval = heartbeat_interval
        self.dissemination_interval = dissemination_interval

class Memberlist(BaseModule):
    def __init__(self, options=MemberlistOptions()):
        super(self.__class__, self).__init__(options=options)
        
    def attach(self, server):
        if self.options.is_controller:
            self._configure_as_controller(server)
        else:
            self._configure_as_heartbeater(server)

    def _configure_as_controller(self, server):
        memberlist = MemberList()
        fault_detector = FaultDetector(logger=server.logger)
        disseminator = MemberlistDisseminator(fault_detector, server.logger)
        dissemination_strategy = DisseminationStrategy(disseminator)
        
        server.add_handler_for_service(HeartbeatServiceStub(memberlist, server.logger))
        server.add_handler_for_service(MemberlistServiceStub(memberlist, server, self.options, server.logger))
        
        self._fault_detector_worker = _FaultDetectorWorker(fault_detector, memberlist, interval=self.options.fault_detection_interval)
        self._fault_detector_worker.start()
        
        self._dissemination_worker = _DisseminationWorker(dissemination_strategy, memberlist, interval=self.options.dissemination_interval)
        self._dissemination_worker.start();
            
    def _configure_as_heartbeater(self, server):
        memberlist = MemberList()
        heartbeater = Heartbeater(server.options.address, server.logger)
        heartbeat_strategy = CentralizedHeartbeatStrategy(heartbeater, self.options.controller_address)

        server.add_handler_for_service(MemberlistServiceStub(memberlist, server, self.options, server.logger))

        self._heartbeat_worker = _HeartbeatWorker(heartbeat_strategy, interval=self.options.heartbeat_interval)
        self._heartbeat_worker.start()
    
    def detach(self, server):
        if self.options.is_controller:
            self._fault_detector_worker.stop()
            self._dissemination_worker.stop()
        else:
            self._heartbeat_worker.stop()

class _HeartbeatWorker(IntervalThread):
    def __init__(self, heartbeating_strategy, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        self._heartbeating_strategy = heartbeating_strategy
        
    def work(self):
        self._heartbeating_strategy.heartbeat()

class _FaultDetectorWorker(IntervalThread):
    def __init__(self, fault_detector, memberlist, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        self._fault_detector = fault_detector
        self._memberlist = memberlist
    
    def work(self):
        self._fault_detector.detect(self._memberlist)

class _DisseminationWorker(IntervalThread):
    def __init__(self, dissemination_strategy, memberlist, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        self._dissemination_strategy = dissemination_strategy
        self._memberlist = memberlist
        
    def work(self):
        self._dissemination_strategy.disseminate(self._memberlist)