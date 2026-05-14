"""

Statement
Check whether or not a linked list contains a cycle. If a cycle exists, return TRUE. Otherwise, return FALSE. The cycle means that at least one node can be reached again by traversing the next pointer.

"""

class Node:
    def __init__(self, val, nxt):
        self.val, self.next = val, nxt

def detect_cycle(head):
    if not head or not head.next: return False
    s, f = head, head
    while s and f and s.next and f.next:
        s = s.next; f = f.next.next
        if s is f: return True
    return False