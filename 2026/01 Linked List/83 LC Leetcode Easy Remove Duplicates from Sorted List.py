"""

83. Remove Duplicates from Sorted List
Solved
Easy
Topics
conpanies icon
Companies
Given the head of a sorted linked list, delete all duplicates such that each element appears only once. Return the linked list sorted as well.



Example 1:


Input: head = [1,1,2]
Output: [1,2]
Example 2:


Input: head = [1,1,2,3,3]
Output: [1,2,3]


Constraints:

The number of nodes in the list is in the range [0, 300].
-100 <= Node.val <= 100
The list is guaranteed to be sorted in ascending order.

Seen this question in a real interview before?
1/6
Yes
No
Accepted
2,371,282/4.2M
Acceptance Rate
56.7%

"""
from typing import Optional


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def skip_repeats(node):
    prev = node
    value = node.val

    while node and node.val == value:
        node = node.next

    prev.next = node
    return node

def delete_duplicates(head):
    if not head: return None

    head.next = delete_duplicates(skip_repeats(head))

    return head


class Solution:
    def deleteDuplicates(self, head: Optional[ListNode]) -> Optional[ListNode]:
        return delete_duplicates(head)