"""

Linked List

"""

from __future__ import annotations
from typing import Optional, Iterator, Iterable


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
            nxt = node.next
            yield node
            node = nxt


def nodes(head: Optional[ListNode]) -> Iterator[ListNode]:
    return iter(head) if head else iter(())


def values(ns: Iterable[ListNode]) -> Iterator[int]:
    return (node.val for node in ns)

def detach_front(head: Optional[ListNode]) -> tuple[Optional[ListNode], Optional[ListNode]]:
    if not head:
        return None, None

    rest = head.next
    head.next = None
    return head, rest

def attach_after(tail: Optional[ListNode], node: ListNode) -> Optional[ListNode]:
    if not tail:
        return None

    tail.next = node
    return node

def cut_after(prev: Optional[ListNode]) -> Optional[ListNode]:
    if not prev:
        return None

    rest = prev.next
    prev.next = None
    return rest

def delete_after(prev: Optional[ListNode]) -> Optional[ListNode]:
    if not prev or not prev.next:
        return None

    target = prev.next
    prev.next = target.next
    target.next = None
    return target

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

def right_middle(head: Optional[ListNode]) -> Optional[ListNode]:
    slow = fast = head

    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next

    return slow

def left_middle(head: Optional[ListNode]) -> Optional[ListNode]:
    if not head:
        return None

    slow, fast = head, head.next
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next

    return slow

def split(head: Optional[ListNode]) -> tuple[Optional[ListNode], Optional[ListNode]]:
    if not head or not head.next:
        return head, None

    mid = left_middle(head)
    right = cut_after(mid)
    return head, right

def sort(a: Optional[ListNode]) -> Optional[ListNode]:
    if not a or not a.next:
        return a

    left, right = split(a)
    return merge(
        sort(left),
        sort(right)
    )



def reverse(head: Optional[ListNode]) -> Optional[ListNode]:
    if not head or not head.next:
        return head

    prev, curr = None, head
    while curr:
        nxt = curr.next
        curr.next = prev
        prev = curr
        curr = nxt

    return prev

def reverse_prefix(head: Optional[ListNode], k: int):
    if k <= 0 or not head:
        return None, None, head

    prev = None
    curr = head
    tail = head

    for _ in range(k):
        if not curr:
            break
        nxt = curr.next
        curr.next = prev
        prev = curr
        curr = nxt

    return prev, tail, curr


def advance(head: Optional[ListNode], k: int):
    for _ in range(k):
        if not head:
            break
        head = head.next

    return head

def reverse_between(head: Optional[ListNode], left: int, right: int):
    if not head or left >= right:
        return head

    dummy = ListNode(0, head)
    before = advance(dummy, left - 1)

    if not before or not before.next:
        return dummy.next

    start = before.next
    rev_head, rev_tail, after = reverse_prefix(
        start,
        right - left + 1
    )

    before.next = rev_head
    rev_tail.next = after

    return dummy.next