import threading
from modules.memberlist.memberlist import Memberlist
from enum import Enum
from collections import namedtuple

class UpdateType(Enum):
    Update = 0
    Delete = 1

Change = namedtuple("Change", ["address", "type", "member"])

class _MemberlistUpdater(object):
    def __init__(self, members, merge=False):
        self._members = members
        self._merge = merge
        self._changes_or_additions = []
        self._deletions = []
        
        self._changes = []

    def add_or_update(self, member):
        self._changes.append(Change(member.address, UpdateType.Update, member))
        
        self._changes_or_additions.append(member)
    
    def delete(self, address):
        self._changes.append(Change(address, UpdateType.Delete, None))
        
        self._deletions.append(address)
    
    def get_memberlist(self):
        members = [member for member in self._members]
        
        for change in self._changes:
            
            for i, member in enumerate(members):
                if member.address == change.address:
                    if change.type == UpdateType.Delete:
                        members.remove(member)
                    elif member.timestamp < change.member.timestamp:
                        members[i] = change.member
                    
                    break
            else:
                members.append(change.member)
        
        return Memberlist(members)

class MemberlistManager(object):
    def __init__(self):
        self._memberlist = Memberlist()
        self._lock = threading.Lock()
    
    def get_copy(self):
        return self._memberlist
    
    def update(self, update_func, merge=False):
        try:
            self._lock.acquire()
            memberlist_updater = _MemberlistUpdater(self._memberlist._members, merge=merge);
            update_func(memberlist_updater)
            self._memberlist = memberlist_updater.get_memberlist()
            return self._memberlist
        finally:
            self._lock.release()