
import unittest
from member import Member
from memberlist import Memberlist, MemberlistException

class MemberlistManagerTest(unittest.TestCase):
    def setUp(self):
        self.member1 = Member('localhost:8080', 1, 1)
        self.member2 = Member('localhost:8088', 1, 1)
        self.memberlist = Memberlist([self.member1, self.member2])
        
    def testMemberlistGet(self):
        member = self.memberlist.get_by_address('localhost:8088')
        self.assertEquals(member, self.member2)

    def testMemberlistGetFail(self):
        with self.assertRaises(MemberlistException):
            self.memberlist.get_by_address('1')


if __name__ == '__main__':
    unittest.main()
    