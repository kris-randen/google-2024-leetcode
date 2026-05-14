"""

725. Split Linked List in Parts
Attempted
Medium

Given the head of a singly linked list and an integer k, split the linked list into k consecutive linked list parts.

The length of each part should be as equal as possible: no two parts should have a size differing by more than one. This may lead to some parts being null.

The parts should be in the order of occurrence in the input list, and parts occurring earlier should always have a size greater than or equal to parts occurring later.

Return an array of the k parts.



Example 1:


Input: head = [1,2,3], k = 5
Output: [[1],[2],[3],[],[]]
Explanation:
The first element output[0] has output[0].val = 1, output[0].next = null.
The last element output[4] is null, but its string representation as a ListNode is [].
Example 2:


Input: head = [1,2,3,4,5,6,7,8,9,10], k = 3
Output: [[1,2,3,4],[5,6,7],[8,9,10]]
Explanation:
The input has been split into consecutive parts with size difference at most 1, and earlier parts are a larger size than the later parts.


Constraints:

The number of nodes in the list is in the range [0, 1000].
0 <= Node.val <= 1000
1 <= k <= 50

Seen this question in a real interview before?
1/6

"""
from typing import Optional, List


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


def length(a):
    return sum(1 for _ in nodes(a))


def size_parts(n, k):
    size, extra = divmod(n, k)
    return [size + (i < extra) for i in range(k)]


def cut_after(prev):
    target = prev.next
    prev.next = None
    return target


def prefix_tail(a, size):
    b = a
    for _ in range(size - 1):
        b = b.next
    return b


def split(a, size):
    if size == 0 or not a:
        return None, a

    tail = prefix_tail(a, size)
    return a, cut_after(tail)


def splits(a, sizes):
    if not sizes:
        return []
    part, rest = split(a, sizes[0])
    return [part] + splits(rest, sizes[1:])


class Solution:
    def splitListToParts(self, head: Optional[ListNode], k: int) -> List[Optional[ListNode]]:
        return \
        (
            splits(
                head,
                size_parts(
                    length(head),
                    k
                )
            )
        )