"""

Statement
Given the head of a singly linked list, return the middle node of the linked list. If the number of nodes in the linked list is even, there will be two middle nodes, so return the second one.

"""

class Node:
    def __init__(self, val, nxt):
        self.val, self.next = val, nxt

def get_middle_node(head):
    if not head or not head.next: return head
    s, f = head, head
    while s and f and s.next and f.next:
        s = s.next; f = f.next.next
    return s