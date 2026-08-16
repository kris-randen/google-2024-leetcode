"""

82. Remove Duplicates from Sorted List II
Solved
Medium

Given the head of a sorted linked list, delete all nodes that have duplicate numbers, leaving only distinct numbers from the original list. Return the linked list sorted as well.


Example 1:


Input: head = [1,2,3,3,4,4,5]
Output: [1,2,5]
Example 2:


Input: head = [1,1,1,2,3]
Output: [2,3]


Constraints:

The number of nodes in the list is in the range [0, 300].
-100 <= Node.val <= 100
The list is guaranteed to be sorted in ascending order.


"""

from collections import Counter
from collections.abc import Callable
from typing import Optional, Set, Iterator, Iterable


class ListNode:
    def __init__(
            self,
            val: int = 0,
            next: Optional[ListNode] = None
    ):
        self.val = val
        self.next = next


def nodes_iter(a: Optional[ListNode]) -> Iterator[ListNode]:
    while a:
        next = a.next
        yield a
        a = next


def values(nodes: Iterable[ListNode]) -> Iterator[int]:
    return (node.val for node in nodes)


def detach_front(a: ListNode) -> tuple[ListNode, Optional[ListNode]]:
    rest = a.next
    a.next = None
    return a, rest


def attach_after(tail: ListNode, node: ListNode) -> ListNode:
    tail.next = node
    node.next = None
    return node


def filter_by_pred(a: Optional[ListNode], pred: Callable[[ListNode], bool]) -> tuple[Optional[ListNode], Optional[ListNode]]:
    true_dummy = true_tail = ListNode()
    false_dummy = false_tail = ListNode()

    while a:
        node, a = detach_front(a)
        if pred(node):
            true_tail = attach_after(true_tail, node)
        else:
            false_tail = attach_after(false_tail, node)

    return true_dummy.next, false_dummy.next


def dupes(a: Optional[ListNode]) -> Set[int]:
    vals = values(nodes_iter(a))
    counter = Counter(vals)
    return {val for val, count in counter.items() if count > 1}


def dedupe(a: Optional[ListNode]) -> Optional[ListNode]:
    vals = dupes(a)
    unique, dupe = filter_by_pred(a, lambda b: b.val not in vals)
    return unique


class Solution:
    def deleteDuplicatesUnsorted(self, head: ListNode) -> ListNode:
        return dedupe(head)
