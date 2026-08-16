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

    def has_next(self) -> bool:
        return self.next is not None

    @property
    def skip(self):
        return self.next if self.has_next() else None

    def cycle_meet(self) -> Optional[ListNode]:
        slow = fast = self
        while has_next(fast):
            slow = slow.next
            fast = fast.skip

            if slow is fast:
                return slow

        return None

    def has_cycle(self) -> bool:
        return self.cycle_meet() is not None

    def __iter__(self):
        node = self
        while node:
            next = node.next
            yield node
            node = next

    def __bool__(self) -> bool:
        return True

    def __len__(self) -> int:
        return \
        (
            float('inf')
            if self.has_cycle() else
            sum(1 for _ in self)
        )


def list_nodes(x: Optional[ListNode]) -> Iterator[ListNode]:
    return iter(x) if x else iter(())


def list_values(xs: Iterable[ListNode]) -> Iterator[int]:
    return (x.val for x in xs)


def detach_front(x: ListNode) -> tuple[ListNode, Optional[ListNode]]:
    rest = x.next
    x.next = None
    return x, rest


def attach_after(tail: ListNode, x: ListNode) -> Optional[ListNode]:
    tail.next = x
    x.next = None
    return x


def has_next(x: Optional[ListNode]) -> bool:
    return x is not None and x.next is not None


def length(x: Optional[ListNode]) -> int:
    return len(x) if x else 0


def tail(x: Optional[ListNode]) -> Optional[ListNode]:
    while has_next(x): x = x.next
    return x