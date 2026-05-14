"""

206. Reverse Linked List
Solved
Easy
Topics
conpanies icon
Companies
Given the head of a singly linked list, reverse the list, and return the reversed list.



Example 1:


Input: head = [1,2,3,4,5]
Output: [5,4,3,2,1]
Example 2:


Input: head = [1,2]
Output: [2,1]
Example 3:

Input: head = []
Output: []


Constraints:

The number of nodes in the list is the range [0, 5000].
-5000 <= Node.val <= 5000


Follow up: A linked list can be reversed either iteratively or recursively. Could you implement both?

"""

# Definition for singly-linked list.
from functools import reduce
from typing import Optional, cast


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

    def __iter__(self):
        node = self
        while node:
            nxt = node.next
            yield node
            node = nxt

    def __str__(self):
        return '[' + ', '.join([f"{node.val}" for node in self]) + ']'

def nodes(head):
    return iter(head) if head else iter(())


def link(vs) -> Optional[ListNode]:
    return reduce(
        lambda nxt, v: ListNode(v, nxt),
        reversed(list(vs)),
        None
    )

def length(head):
    return sum(1 for _ in nodes(head))

def values(head):
    return (node.val for node in nodes(head))

def unlink(head):
    return list(values(head))

def reverse(head):
    prev = None

    for node in nodes(head):
        node.next = prev
        prev = node

    return prev

def rev(head):
    def reverse_rec(curr):
        if curr is None or curr.next is None: return curr, curr
        new_head, new_tail = reverse_rec(curr.next)
        curr.next = None
        new_tail.next = curr
        return new_head, curr

    rev_head, rev_tail = reverse_rec(head)
    return rev_head



if __name__ == '__main__':
    nums = [1, 2, 3, 4]
    ls = link(nums)
    us = unlink(ls)
    assert (nums == us)
    print(rev(ls))
