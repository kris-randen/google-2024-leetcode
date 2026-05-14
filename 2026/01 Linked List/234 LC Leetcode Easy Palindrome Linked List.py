"""

234. Palindrome Linked List
Easy
Topics
conpanies icon
Companies
Given the head of a singly linked list, return true if it is a palindrome or false otherwise.



Example 1:


Input: head = [1,2,2,1]
Output: true
Example 2:


Input: head = [1,2]
Output: false


Constraints:

The number of nodes in the list is in the range [1, 105].
0 <= Node.val <= 9


Follow up: Could you do it in O(n) time and O(1) space?

Seen this question in a real interview before?
1/6
Yes
No
Accepted
2,893,316/5M
Acceptance Rate
57.8%

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

def values(head):
    return [node.val for node in nodes(head)]

def palindrome(head):
    return (
    all(
        u == v for u, v in
        zip(
            values(head),
            reversed(values(head))
        )
    ))

class Solution:
    def isPalindrome(self, head: Optional[ListNode]) -> bool:
        return palindrome(head)
