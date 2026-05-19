"""

Linked List

"""

from __future__ import annotations
from typing import List, Optional, Iterator, Iterable


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


def nodes(head: Optional[ListNode]) -> Iterator[ListNode]:
    return iter(head) if head else iter(())

def values(ns: Iterable[ListNode]) -> Iterator[int]:
    return (node.val for node in ns)

def detach_front(head: Optional[ListNode]) -> tuple[Optional[ListNode], Optional[ListNode]]:
    if not head or not head.next:
        return head, None

    rest = head.next
    head.next = None
    return head, rest

def attach_after(tail: Optional[ListNode], node: Optional[ListNode]) -> Optional[ListNode]:
    if not tail:
        return None

    tail.next = node
    node.next = None
    return node

def cut_after(prev: Optional[ListNode]) -> Optional[ListNode]:
    if not prev or not prev.next:
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

def sort(head: Optional[ListNode]) -> Optional[ListNode]:
    if not head or not head.next:
        return head

    left, right = split(head)
    return merge(
        sort(left),
        sort(right)
    )


def reverse(head: Optional[ListNode]) -> Optional[ListNode]:
    if not head or not head.next:
        return head

    prev = None
    curr = head

    while curr:
        next = curr.next
        curr.next = prev
        prev = curr
        curr = next

    return prev

def reverse_prefix(head: Optional[ListNode], k: int) -> tuple[Optional[ListNode], Optional[ListNode], Optional[ListNode]]:
    if k <= 0 or not head:
        return None, None, head

    prev = None
    curr = head
    tail = head

    for _ in range(k):
        if not curr:
            break
        next = curr.next
        curr.next = prev
        prev = curr
        curr = next

    return prev, tail, curr


def advance(head: Optional[ListNode], k: int) -> Optional[ListNode]:
    if k <= 0 or not head:
        return head

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
    length = right - left + 1

    rev_head, rev_tail, after = reverse_prefix(start, length)

    before.next = rev_head
    rev_tail.next = after

    return dummy.next


def has_k_nodes(head: Optional[ListNode], k: int) -> bool:
    if k <= 0:
        return True

    return advance(head, k - 1) is not None

def remove_kth_from_the_end(head: Optional[ListNode], k: int):
    if not head or k <= 0 or not has_k_nodes(head, k):
        return head

    dummy = ListNode(0, head)
    slow = fast = dummy

    fast = advance(dummy, k + 1)
    while fast:
        slow = slow.next
        fast = fast.next

    delete_after(slow)

    return dummy.next


def reverse_nodes_in_k_group(head: Optional[ListNode], k: int):
    if not head or k <= 1:
        return head

    dummy = ListNode(0, head)
    group_prev = dummy

    while has_k_nodes(group_prev, k):
        start = group_prev.next
        rev_head, rev_tail, after = reverse_prefix(start, k)
        group_prev.next = rev_head
        rev_tail.next = after
        group_prev = rev_tail

    return dummy.next