
import unittest
from member import Member, MemberState
from memberlist_manager import MemberlistManager

class MemberlistManagerTest(unittest.TestCase):
    def setUp(self):
        self.manager = MemberlistManager()
        
    def testAddMember(self):
        self._add_member('localhost', 1, 2)
        
        memberlist = self.manager.get_copy()
        self.assertEquals(len(memberlist), 1)
        
    def testUpdateMember(self):
        self._add_member('localhost', 1, 2)
        self._add_member('localhost2', 1, 2)
        self._add_member('localhost2', 2, 3)
        
        memberlist = self.manager.get_copy()
        self.assertEquals(len(memberlist), 2)
        self.assertEquals(memberlist.get_by_address('localhost2').seq_num, 2)
        
    def testDeleteMember(self):
        self._add_member('localhost1', 1, 2)
        self._add_member('localhost2', 2, 3)
        
        self._delete_member('localhost2')
        
        memberlist = self.manager.get_copy()
        self.assertEquals(len(memberlist), 1)
        self.assertEquals(memberlist.get_by_address('localhost1').seq_num, 1)
        
    def _add_member(self, address, seq_num=1, timestamp=1, state=MemberState.Undefined):
        def update_func(updater):
            updater.add_or_update(Member(address, seq_num, timestamp, state))
        self.manager.update(update_func)
        
    def _delete_member(self, address):
        def update_func(updater):
            updater.delete(address)
        self.manager.update(update_func)

if __name__ == '__main__':
    unittest.main()
    