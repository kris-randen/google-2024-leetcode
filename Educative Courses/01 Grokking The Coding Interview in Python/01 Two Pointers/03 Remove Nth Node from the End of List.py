"""
Statement
Given a singly linked list, remove the nth
node from the end of the list and return its head.

Constraints:

The number of nodes in the list is k.
1 ≤ n ≤ k
"""

def remove_nth_last_node(head, n):
  if not head or not n: return head
  l, r = head, head
  while n >= 0 and r:
    r = r.next; n -= 1
  if n < 0:
    while r:
      l = l.next; r = r.next
    l.next = l.next.next
  else:
    head = head.next
  return head
