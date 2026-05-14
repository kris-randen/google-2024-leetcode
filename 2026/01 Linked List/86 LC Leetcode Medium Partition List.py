"""

86. Partition List
Medium
Companies
Given the head of a linked list and a value x, partition it such that all nodes less than x come before nodes greater than or equal to x.

You should preserve the original relative order of the nodes in each of the two partitions.



Example 1:


Input: head = [1,4,3,2,5,2], x = 3
Output: [1,2,2,4,3,5]
Example 2:

Input: head = [2,1], x = 2
Output: [1,2]


Constraints:

The number of nodes in the list is in the range [0, 200].
-100 <= Node.val <= 100
-200 <= x <= 200

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

def attach_after(tail, b):
    tail.next = b
    return b

def partition_by_predicate(a, pred):
    true_dummy = true_tail = ListNode()
    false_dummy = false_tail = ListNode()

    while a:
        node, a = detach_front(a)

        if pred(node):
            true_tail = attach_after(true_tail, node)
        else:
            false_tail = attach_after(false_tail, node)

    return true_dummy.next, true_tail, false_dummy.next, false_tail

def partition(a, x):
    less, tail_less, greater, tail_greater = partition_by_predicate(a, lambda a: a.val < x)

    if less is None:
        return greater

    tail_less.next = greater
    return less


class Solution:
    def partition(self, head: Optional[ListNode], x: int) -> Optional[ListNode]:
        less, tail_less, greater, tail_greater = partition_by_predicate(head, lambda a: a.val < x)

        if less is None:
            return greater

        tail_less.next = greater
        return less
