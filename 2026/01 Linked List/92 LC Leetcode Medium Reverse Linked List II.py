"""

92. Reverse Linked List II
Solved
Medium

Given the head of a singly linked list and two integers left and right where left <= right, reverse the nodes of the list from position left to position right, and return the reversed list.



Example 1:


Input: head = [1,2,3,4,5], left = 2, right = 4
Output: [1,4,3,2,5]
Example 2:

Input: head = [5], left = 1, right = 1
Output: [5]


Constraints:

The number of nodes in the list is n.
1 <= n <= 500
-500 <= Node.val <= 500
1 <= left <= right <= n


Follow up: Could you do it in one pass?

Seen this question in a real interview before?
1/6
Yes
No
Accepted
1,312,903/2.6M
Acceptance Rate
51.4%

"""
from typing import Optional


# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def advance(head, k):
    curr = head
    for _ in range(k):
        curr = curr.next
    return curr

def reverse_prefix(head, k):
    prev, curr, tail = None, head, head

    for _ in range(k):
        next = curr.next
        curr.next = prev
        prev = curr
        curr = next

    return prev, tail, curr


def reverse_between(head, left, right):
    if head is None or left == right:
        return head

    dummy = ListNode(0, head)
    before = advance(head, left - 1)
    rev_head, rev_tail, after = reverse_prefix(
                                    before.next,
                                    right - left + 1)
    before.next = rev_head
    rev_tail.next = after

    return dummy.next

class Solution:
    def reverseBetween(self, head: Optional[ListNode], left: int, right: int) -> Optional[ListNode]:
        return reverse_between(head, left, right)
