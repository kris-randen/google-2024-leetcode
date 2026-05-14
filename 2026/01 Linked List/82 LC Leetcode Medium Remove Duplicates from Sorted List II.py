"""

82. Remove Duplicates from Sorted List II
Medium
Given the head of a sorted linked list, delete all nodes that have duplicate numbers, leaving only distinct numbers from the original list. Return the linked list sorted as well.



Example 1:


Input: head = [1,2,3,3,4,4,5]
Output: [1,2,5]
Example 2:


Input: head = [1,1,1,2,3]
Output: [2,3]


Constraints:

The number of nodes in the list is in the range [0, 300].
-100 <= Node.val <= 100
The list is guaranteed to be sorted in ascending order.

Seen this question in a real interview before?
1/6
Yes
No
Accepted
1,098,785/2.1M
Acceptance Rate
51.7%

"""
from typing import Optional


# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def repeats(head):
    return (
            head is not None and
            head.next is not None and
            head.val == head.next.val
    )


def skip_repeats(node):
    value = node.val

    while node is not None and node.val == value:
        node = node.next

    return node

def delete_duplicates(head):
    if head is None:
        return None

    if repeats(head):
        return delete_duplicates(skip_repeats(head))

    head.next = delete_duplicates(head.next)
    return head

class Solution:
    def deleteDuplicates(self, head: Optional[ListNode]) -> Optional[ListNode]:
        return delete_duplicates(head)
