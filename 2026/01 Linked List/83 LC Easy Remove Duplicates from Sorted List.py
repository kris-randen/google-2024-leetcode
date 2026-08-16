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
2,392,583/4.2M
Acceptance Rate
56.7%

"""

from __future__ import annotations
from typing import Optional

class ListNode:
    def __init__(
            self,
            val: int = 0,
            next: Optional[ListNode] = None
    ):
        self.val = val
        self.next = next


def delete_after(prev: ListNode) -> Optional[ListNode]:
    target = prev.next
    if not target:
        return target

    prev.next = target.next
    target.next = None
    return target

def dedupe_sorted(head: Optional[ListNode]) -> Optional[ListNode]:
    curr = head
    while curr and curr.next:
        if curr.val == curr.next.val:
            delete_after(curr)
        else:
            curr = curr.next

    return head


class Solution:
    def deleteDuplicates(self, head: Optional[ListNode]) -> Optional[ListNode]:
        return dedupe_sorted(head)


