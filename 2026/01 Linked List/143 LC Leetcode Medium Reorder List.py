"""

143. Reorder List
Solved
Medium
Topics
conpanies icon
Companies
You are given the head of a singly linked-list. The list can be represented as:

L0 → L1 → … → Ln - 1 → Ln
Reorder the list to be on the following form:

L0 → Ln → L1 → Ln - 1 → L2 → Ln - 2 → …
You may not modify the values in the list's nodes. Only nodes themselves may be changed.



Example 1:


Input: head = [1,2,3,4]
Output: [1,4,2,3]
Example 2:


Input: head = [1,2,3,4,5]
Output: [1,5,2,4,3]


Constraints:

The number of nodes in the list is in the range [1, 5 * 104].
1 <= Node.val <= 1000

"""
from typing import Optional


# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next



def nodes(head):
    while head:
        nxt = head.next
        yield head
        head = nxt


def detach_front(head):
    rest = head.next
    head.next = None
    return head, rest

def attach_after(tail, rest):
    tail.next = rest
    return rest

def cut_after(prev):
    target = prev.next
    prev.next = None
    return target

def weave(a, b):
    dummy = tail = ListNode()

    while a or b:
        if a:
            node, a = detach_front(a)
            tail = attach_after(tail, node)
        if b:
            node, b = detach_front(b)
            tail = attach_after(tail, node)

    return dummy.next

def middle(head):
    slow = fast = head

    while fast and fast.next:
        slow, fast = slow.next, fast.next.next

    return slow

def reverse(head):
    prev = None

    for node in nodes(head):
        node.next = prev
        prev = node

    return prev

def split(head):
    if not head or not head.next:
        return head, None

    mid = middle(head)
    rest = cut_after(mid)
    return head, rest

def reorder(head):
    a, b = split(head)
    return \
    (
        weave(
            a,
            reverse(b)
        )
    )

class Solution:
    def reorderList(self, head: Optional[ListNode]) -> None:
        """
        Do not return anything, modify head in-place instead.
        """
        return reorder(head)
