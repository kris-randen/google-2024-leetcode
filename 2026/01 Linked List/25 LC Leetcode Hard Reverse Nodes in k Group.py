"""

25. Reverse Nodes in k-Group
Solved
Hard

Given the head of a linked list, reverse the nodes of the list k at a time, and return the modified list.

k is a positive integer and is less than or equal to the length of the linked list. If the number of nodes is not a multiple of k then left-out nodes, in the end, should remain as it is.

You may not alter the values in the list's nodes, only nodes themselves may be changed.



Example 1:


Input: head = [1,2,3,4,5], k = 2
Output: [2,1,4,3,5]
Example 2:


Input: head = [1,2,3,4,5], k = 3
Output: [3,2,1,4,5]


Constraints:

The number of nodes in the list is n.
1 <= k <= n <= 5000
0 <= Node.val <= 1000


Follow-up: Can you solve the problem in O(1) extra memory space?


Seen this question in a real interview before?
1/6
Yes
No
Accepted
1,534,836/2.3M
Acceptance Rate
65.9%

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

def has_k_nodes(head, k):
    for _ in range(k):
        if head is None:
            return False
        head = head.next
    return True


def reverse_prefix(head, k):
    prev, curr = None, head

    for _ in range(k):
        nxt = curr.next
        curr.next = prev
        prev = curr
        curr = nxt

    return prev, head, curr

def reverse_k_group(head, k):
    if not has_k_nodes(head, k):
        return head

    rev_head, rev_tail, after = reverse_prefix(head, k)
    rev_tail.next = reverse_k_group(after, k)
    return rev_head

class Solution:
    def reverseKGroup(self, head: Optional[ListNode], k: int) -> Optional[ListNode]:
        return reverse_k_group(head, k)

