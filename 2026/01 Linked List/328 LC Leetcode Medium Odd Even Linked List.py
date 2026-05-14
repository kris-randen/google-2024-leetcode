"""

328. Odd Even Linked List
Medium
Given the head of a singly linked list, group all the nodes with odd indices together followed by the nodes with even indices, and return the reordered list.

The first node is considered odd, and the second node is even, and so on.

Note that the relative order inside both the even and odd groups should remain as it was in the input.

You must solve the problem in O(1) extra space complexity and O(n) time complexity.



Example 1:


Input: head = [1,2,3,4,5]
Output: [1,3,5,2,4]
Example 2:


Input: head = [2,1,3,5,6,4,7]
Output: [2,3,6,7,1,5,4]


Constraints:

The number of nodes in the linked list is in the range [0, 104].
-106 <= Node.val <= 106

"""
from typing import Optional


# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def detach_front(a):
    rest = a.next
    a.next = None
    return a, rest


def attach_after(tail, a):
    tail.next = a
    return a


def partition_odd_even(a):
    odd_dummy = odd_tail = ListNode()
    even_dummy = even_tail = ListNode()
    index = 1

    while a:
        node, a = detach_front(a)
        if index % 2 == 1:
            odd_tail = attach_after(odd_tail, node)
        else:
            even_tail = attach_after(even_tail, node)
        index += 1

    return odd_dummy.next, odd_tail, even_dummy.next, even_tail

class Solution:
    def oddEvenList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        odd, odd_tail, even, even_tail = partition_odd_even(head)
        if odd is None:
            return even
        odd_tail.next = even
        return odd
