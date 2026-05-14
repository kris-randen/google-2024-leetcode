"""

2074. Reverse Nodes in Even Length Groups
Medium
You are given the head of a linked list.

The nodes in the linked list are sequentially assigned to non-empty groups whose lengths form the sequence of the natural numbers (1, 2, 3, 4, ...). The length of a group is the number of nodes assigned to it. In other words,

The 1st node is assigned to the first group.
The 2nd and the 3rd nodes are assigned to the second group.
The 4th, 5th, and 6th nodes are assigned to the third group, and so on.
Note that the length of the last group may be less than or equal to 1 + the length of the second to last group.

Reverse the nodes in each group with an even length, and return the head of the modified linked list.


Example 1:


Input: head = [5,2,6,3,9,1,7,3,8,4]
Output: [5,6,2,3,9,1,4,8,3,7]
Explanation:
- The length of the first group is 1, which is odd, hence no reversal occurs.
- The length of the second group is 2, which is even, hence the nodes are reversed.
- The length of the third group is 3, which is odd, hence no reversal occurs.
- The length of the last group is 4, which is even, hence the nodes are reversed.
Example 2:


Input: head = [1,1,0,6]
Output: [1,0,1,6]
Explanation:
- The length of the first group is 1. No reversal occurs.
- The length of the second group is 2. The nodes are reversed.
- The length of the last group is 1. No reversal occurs.
Example 3:


Input: head = [1,1,0,6,5]
Output: [1,0,1,5,6]
Explanation:
- The length of the first group is 1. No reversal occurs.
- The length of the second group is 2. The nodes are reversed.
- The length of the last group is 2. The nodes are reversed.


Constraints:

The number of nodes in the list is in the range [1, 105].
0 <= Node.val <= 105

Seen this question in a real interview before?
1/6
Yes
No
Accepted
46,361/72.5K
Acceptance Rate
63.9%

"""
from operator import length_hint
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


def length(head):
    return sum(1 for _ in nodes(head))


def partition(n):
    index, total, parts = 1, 0, []

    while total < n:
        rem = n - total
        parts += [index if rem > index else rem]
        total += index
        index += 1

    return parts


def advance(head, k):
    for _ in range(k):
        if head is None:
            return head
        head = head.next
    return head


def reverse_prefix(head, k):
    prev, curr = None, head

    for _ in range(k):
        nxt = curr.next
        curr.next = prev
        prev = curr
        curr = nxt

    return prev, head, curr


def reverse(head, k):
    rev_head, rev_tail, after = reverse_prefix(head, k)
    rev_tail.next = after
    return rev_tail


def reverse_even_length_groups(head):
    dummy = ListNode(0, head)
    prev = dummy
    for part in partition(length(head)):
        if part % 2 == 1:
            prev = advance(prev, part)
        else:
            rev_head, rev_tail, after = reverse_prefix(prev.next, part)
            prev.next = rev_head
            rev_tail.next = after
            prev = rev_tail
    return head


class Solution:
    def reverseEvenLengthGroups(self, head: Optional[ListNode]) -> Optional[ListNode]:
        return reverse_even_length_groups(head)