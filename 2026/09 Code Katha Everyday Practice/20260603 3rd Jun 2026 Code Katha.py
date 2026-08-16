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


def list_nodes(a: Optional[ListNode]) -> Iterator[ListNode]:
    return iter(a) if a else iter(())


def values(nodes: Iterable[ListNode]) -> Iterator[int]:
    return (node.val for node in nodes)


def detach_front(a: ListNode) -> tuple[ListNode, Optional[ListNode]]:
    rest = a.next
    a.next = None
    return a, rest


def attach_after(tail: ListNode, a: ListNode) -> ListNode:
    tail.next = a
    a.next = None
    return a


def cut_after(prev: ListNode) -> Optional[ListNode]:
    rest = prev.next
    prev.next = None
    return rest


def delete_after(prev: ListNode) -> Optional[ListNode]:
    target = prev.next
    if not target: return None

    prev.next = target.next
    target.next = None
    return target


def advance(a: Optional[ListNode], k: int) -> Optional[ListNode]:
    if not a or k <= 0:
        return a

    for _ in range(k):
        if not a: break
        a = a.next

    return a


def has_k_nodes(a: Optional[ListNode], k: int) -> bool:
    return k <= 0 or advance(a, k - 1) is not None


def right_middle(a: Optional[ListNode]) -> Optional[ListNode]:
    slow = fast = a
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    return slow


def left_middle(a: Optional[ListNode]) -> Optional[ListNode]:
    if not a: return a

    slow, fast = a, a.next
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    return slow


def split(a: Optional[ListNode]) -> tuple[Optional[ListNode], Optional[ListNode]]:
    if not a: return a, None

    mid = left_middle(a)
    right = cut_after(mid)
    return a, right


def weave(a: Optional[ListNode], b: Optional[ListNode]) -> Optional[ListNode]:
    dummy = tail = ListNode()

    while a or b:
        if a:
            node, a = detach_front(a)
            tail = attach_after(tail, node)
        if b:
            node, b = detach_front(b)
            tail = attach_after(tail, node)

    return dummy.next


def merge(a: Optional[ListNode], b: Optional[ListNode]) -> Optional[ListNode]:
    dummy = tail = ListNode()

    while a and b:
        if a.val <= b.val:
            node, a = detach_front(a)
        else:
            node, b = detach_front(b)
        tail = attach_after(tail, node)

    tail.next = a or b
    return dummy.next


def sort(a: Optional[ListNode]) -> Optional[ListNode]:
    if not a or not a.next: return a

    left, right = split(a)
    return merge(
        sort(left),
        sort(right)
    )


def reverse(a: Optional[ListNode]) -> Optional[ListNode]:
    prev, curr = None, a
    while curr:
        next = curr.next
        curr.next = prev
        prev = curr
        curr = next
    return prev


def reverse_prefix(a: Optional[ListNode], k: int) -> \
    tuple[Optional[ListNode], Optional[ListNode], Optional[ListNode]]:
    if not a or k <= 0: return None, None, a

    prev, tail, curr = None, a, a
    for _ in range(k):
        if not curr: break
        next = curr.next
        curr.next = prev
        prev = curr
        curr = next
    return prev, tail, curr


def reverse_between(a: Optional[ListNode], left: int, right: int) -> Optional[ListNode]:
    if not a or left >= right or not has_k_nodes(a, left):
        return a

    dummy = ListNode(0, a)
    before = advance(dummy, left - 1)
    start = before.next
    length = right - left + 1

    rhead, rtail, after = reverse_prefix(start, length)
    before.next = rhead
    rtail.next = after
    return dummy.next


def reverse_in_k_groups(a: Optional[ListNode], k: int) -> Optional[ListNode]:
    if not a or k <= 1: return a

    dummy = ListNode(0, a)
    before = dummy
    start = before.next

    while has_k_nodes(start, k):
        rhead, rtail, after = reverse_prefix(start, k)

        before.next = rhead
        rtail.next = after

        before = rtail
        start = before.next

    return dummy.next


def cycle_meet(a: Optional[ListNode]) -> Optional[ListNode]:
    if not a or not a.next: return None

    slow = fast = a
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next

        if slow is fast:
            return slow

    return None


def has_cycle(a: Optional[ListNode]) -> bool:
    return cycle_meet(a) is not None


def cycle_start(a: Optional[ListNode]) -> Optional[ListNode]:
    meet = cycle_meet(a)
    if not meet: return None
    
    slow, fast = a, meet
    while slow is not fast:
        slow = slow.next
        fast = fast.next
    return slow


def remove_kth_from_end(a: Optional[ListNode], k: int) -> Optional[ListNode]:
    if not a or k <= 0 or not has_k_nodes(a, k):
        return a

    dummy = ListNode(0, a)
    slow = fast = dummy
    fast = advance(fast, k)

    while fast and fast.next:
        slow = slow.next
        fast = fast.next

    delete_after(slow)
    return dummy.next