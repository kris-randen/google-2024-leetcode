"""

02 Remove n-th Node From the End of a Singly Linked List

"""

from linked_list import LinkedList
from linked_list_node import LinkedListNode

def remove_nth_last_node(head, n):
    l = r = head; c = 0
    while c <= n and r:
        c += 1; r = r.next

    if c <= n:
      return head.next

    while not r is None:
        l = l.next; r = r.next
    l.next = l.next.next
    return head























