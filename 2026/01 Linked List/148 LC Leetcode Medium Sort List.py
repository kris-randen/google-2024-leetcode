"""

148. Sort List
Medium
Topics
conpanies icon
Companies
Given the head of a linked list, return the list after sorting it in ascending order.



Example 1:


Input: head = [4,2,1,3]
Output: [1,2,3,4]
Example 2:


Input: head = [-1,5,3,4,0]
Output: [-1,0,3,4,5]
Example 3:

Input: head = []
Output: []


Constraints:

The number of nodes in the list is in the range [0, 5 * 104].
-105 <= Node.val <= 105


Follow up: Can you sort the linked list in O(n logn) time and O(1) memory (i.e. constant space)?

"""

from typing import Optional

# Definition for singly-linked list.
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

def cut_after(prev):
    target = prev.next
    prev.next = None
    return target

def middle(head):
    if not head: return head

    slow, fast = head, head.next

    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next

    return slow


def split(head):
    mid = middle(head)
    rest = cut_after(mid)
    return head, rest

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

def merge_sort(head):
    if head is None or head.next is None:
        return head

    left, right = split(head)

    return \
    (
        merge(
            merge_sort(left),
            merge_sort(right)
        )
    )


class Solution:
    def sortList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        return merge_sort(head)
