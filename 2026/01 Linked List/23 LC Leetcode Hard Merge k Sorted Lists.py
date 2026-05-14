"""

23. Merge k Sorted Lists
Solved
Hard

You are given an array of k linked-lists lists, each linked-list is sorted in ascending order.

Merge all the linked-lists into one sorted linked-list and return it.



Example 1:

Input: lists = [[1,4,5],[1,3,4],[2,6]]
Output: [1,1,2,3,4,4,5,6]
Explanation: The linked-lists are:
[
  1->4->5,
  1->3->4,
  2->6
]
merging them into one sorted linked list:
1->1->2->3->4->4->5->6
Example 2:

Input: lists = []
Output: []
Example 3:

Input: lists = [[]]
Output: []


Constraints:

k == lists.length
0 <= k <= 104
0 <= lists[i].length <= 500
-104 <= lists[i][j] <= 104
lists[i] is sorted in ascending order.
The sum of lists[i].length will not exceed 104.

"""
from functools import cmp_to_key
from heapq import heapify, heappop, heappush
from typing import List, Optional


# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def nodes(a):
    while a:
        next = a.next
        yield a
        a = next

def detach_front(b):
    if not b: return None, None
    rest = b.next
    b.next = None
    return b, rest

def attach_after(tail, b):
    if not b: return None
    tail.next = b
    return b

def frontier(bs):
    return [(i, b) for (i, b) in enumerate(bs) if b is not None]

def select(ibs):
    return min(ibs, key=lambda ib: ib[1].val)

def merges(bs):
    dummy = tail = ListNode()

    while (fs := frontier(bs)):
        i, f = select(fs)
        node, a = detach_front(f)
        bs[i] = a
        tail = attach_after(tail, node)

    return dummy.next

def heap_links(bs):
    heap = [
        (node.val, i, node)
        for i, node in
        enumerate(bs)
    ]
    heapify(heap)
    return heap

def merges_heap(heap):
    dummy = tail = ListNode()

    while heap:
        a = heappop(heap)
        node, a = detach_front(a)
        if a: heappush(a)
        tail = attach_after(tail, node)

    return dummy.next


class Solution:
    def mergeKLists(self, lists: List[Optional[ListNode]]) -> Optional[ListNode]:
        return \
        (
            merges_heap(
                heap_links(lists)
            )
        )
