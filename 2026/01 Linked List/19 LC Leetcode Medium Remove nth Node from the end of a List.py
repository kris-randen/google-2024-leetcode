"""

19. Remove Nth Node From End of List
Solved
Medium
Given the head of a linked list, remove the nth node from the end of the list and return its head.



Example 1:


Input: head = [1,2,3,4,5], n = 2
Output: [1,2,3,5]
Example 2:

Input: head = [1], n = 1
Output: []
Example 3:

Input: head = [1,2], n = 1
Output: [1]


Constraints:

The number of nodes in the list is sz.
1 <= sz <= 30
0 <= Node.val <= 100
1 <= n <= sz


Follow up: Could you do this in one pass?

"""
from functools import reduce
from typing import Optional

"""

2 Pointers Approach. Use to pointers l and r starting from head. Move r to the right n + 1 steps from l. Then move both of them together until r is at the end. Then l is pointing to the n-th node from the end. Remember we don't want l to be the nth node from the end but the one before it so we can remove it using the linked list next pointer from l.

2 Important corner cases to consider
1. There are not n nodes in the list (this is clearly not the case as the constraints state it)
2. The list has exactly n nodes in which case we need to remove the head and return the pointer to its next element

All other mismatch corner cases are avoided by safe data guarantee in the problem

"""


# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def itr_nodes(head):
    while head:
        nxt = head.next
        yield head
        head = nxt


def const(node, nxt):
    node.next = nxt
    return node


def unlink(head):
    return list(itr_nodes(head))


def link(nodes):
    return reduce(
        lambda nxt, node: const(node, nxt),
        reversed(nodes),
        None
    )


def remove_nth_list(vs, n):
    vs.pop(len(vs) - n)
    return vs


def remove_nth_link(head, n):
    return (
        link(
            remove_nth_list(
                unlink(head), n
            )
        ))


def remove_nth(head, n):
    l, r, c = head, head, 0

    while r and c < n + 1:
        r, c = r.next, c + 1

    if c < n + 1:
        return head.next

    while r:
        l, r = l.next, r.next

    l.next = l.next.next
    return head


def delete_after(prev):
    target = prev.next
    if target is None:
        return None

    prev.next = target.next
    return target


def remove_nth_from_end(a, n):
    dummy = ListNode(0, a)
    left = right = dummy

    for _ in range(n + 1):
        right = right.next

    while right:
        left = left.next
        right = right.next

    delete_after(left)
    return dummy.next



class Solution:
    def removeNthFromEnd(self, head: Optional[ListNode], n: int) -> Optional[ListNode]:
        return remove_nth_link(head, n)
