"""

Code Katha

"""


from __future__ import annotations
from typing import Optional, Iterator, Iterable


"""

Linked List

"""


class ListNode:
    def __init__(
            self,
            val: int = 0,
            next: Optional[ListNode] = None
    ):
        self.val = val
        self.next = next

    def __iter__(self):
        node = self
        while node:
            next = node.next
            yield node
            node = next


def list_nodes(x: Optional[ListNode]) -> Iterator[ListNode]:
    return iter(x) if x else iter(())


def list_values(xs: Iterable[ListNode]) -> Iterator[int]:
    return (x.val for x in xs)


def detach_front(x: ListNode) -> tuple[ListNode, Optional[ListNode]]:
    rest = x.next
    x.next = None
    return x, rest


def attach_after(tail: ListNode, x: ListNode) -> ListNode:
    tail.next = x
    x.next = None
    return x


def cut_after(prev: ListNode) -> Optional[ListNode]:
    rest = prev.next
    prev.next = None
    return rest


def delete_after(prev: ListNode) -> Optional[ListNode]:
    target = prev.next
    if not target:
        return None

    prev.next = target.next
    target.next = None
    return target


def advance(x: Optional[ListNode], k: int) -> Optional[ListNode]:
    if not x or k <= 0:
        return x

    for _ in range(k):
        if not x: break
        x = x.next
    return x


def has_k_nodes(x: Optional[ListNode], k: int) -> bool:
    return k <= 0 or advance(x, k - 1) is not None




































