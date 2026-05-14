"""

21. Merge Two Sorted Lists
Solved
Easy
Companies
You are given the heads of two sorted linked lists list1 and list2.

Merge the two lists into one sorted list. The list should be made by splicing together the nodes of the first two lists.

Return the head of the merged linked list.



Example 1:


Input: list1 = [1,2,4], list2 = [1,3,4]
Output: [1,1,2,3,4,4]
Example 2:

Input: list1 = [], list2 = []
Output: []
Example 3:

Input: list1 = [], list2 = [0]
Output: [0]


Constraints:

The number of nodes in both lists is in the range [0, 50].
-100 <= Node.val <= 100
Both list1 and list2 are sorted in non-decreasing order.

Seen this question in a real interview before?
1/6
Yes
No
Accepted
6,235,208/9.1M
Acceptance Rate
68.2%

"""
from typing import Optional


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def detach_front(head):
    rest = head.next
    head.next = None
    return head, rest

def attach_after(tail, node):
    tail.next = node
    return node

def merge(a, b):
    dummy = tail = ListNode()

    while a and b:
        if a.val <= b.val:
            node, a = detach_front(a)
        else:
            node, b = detach_front(b)
        tail = attach_after(tail, node)

    tail.next = a or b
    return dummy.next

class Solution:
    def mergeTwoLists(self, list1: Optional[ListNode], list2: Optional[ListNode]) -> Optional[ListNode]:
        return merge(list1, list2)


