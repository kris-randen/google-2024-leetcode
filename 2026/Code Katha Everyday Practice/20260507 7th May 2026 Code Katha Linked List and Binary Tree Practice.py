"""

Linked List

"""

from __future__ import annotations
from typing import Optional, Iterator, List, Iterable


class ListNode:
    def __init__(self, val: int=0, next: Optional[ListNode]=None):
        self.val = val
        self.next = next

    def __iter__(self):
        node = self

        while node:
            next = node.next
            yield node
            node = next


def nodes_iter(head: Optional[ListNode]) -> Iterator[ListNode]:
    return iter(head) if head else iter(())

def values_iter(nodes: Iterable[ListNode]) -> Iterator[int]:
    return (node.val for node in nodes)

def detach_front(head: ListNode) -> tuple[Optional[ListNode], Optional[ListNode]]:
    rest = head.next
    head.next = None
    return head, rest

def attach_after(tail: ListNode, new_tail: ListNode) -> Optional[ListNode]:
    tail.next = new_tail
    new_tail.next = None
    return new_tail

def cut_after(prev: ListNode):
    rest = prev.next
    prev.next = None
    return rest

def delete_after(prev: ListNode):
    target = prev.next

    if not target:
        return None

    prev.next = target.next
    target.next = None
    return target

def move_slow_fast(slow: ListNode, fast: ListNode):
    return slow.next, fast.next.next

def right_middle(head: Optional[ListNode]):
    slow = fast = head

    while fast and fast.next:
        slow, fast = move_slow_fast(slow,fast)

    return slow


def left_middle(head: Optional[ListNode]):
    if head is None:
        return None

    slow, fast = head, head.next

    while fast and fast.next:
        slow, fast = move_slow_fast(slow, fast)

    return slow


def split(head: Optional[ListNode]) -> tuple[Optional[ListNode], Optional[ListNode]]:
    if not head or not head.next:
        return head, None

    mid = left_middle(head)
    rest = cut_after(mid)

    return head, rest

def reverse(head: Optional[ListNode]):
    prev, curr = None, head

    while curr:
        next = curr.next
        curr.next = prev
        prev = curr
        curr = next

    return prev


# return reversed head, reverse tail and the after part so the caller can use and connect them appropriately
def reverse_prefix(head: Optional[ListNode], k: int):
    prev, after, tail = None, head, head

    for _ in range(k):
        if after is None:
            raise ValueError(f"The list doesn't have k = {k} nodes.")

        next = after.next
        after.next = prev
        prev = after
        after = next

    return prev, tail, after


def find_nth_from_end(head: Optional[ListNode], n: int):
    slow = fast = head

    for _ in range(n):
        if not fast:
            raise ValueError(f"The list doesn't have n = {n} nodes.")
        fast = fast.next

    while fast:
        slow, fast = slow.next, fast.next

    return slow


def remove_nth_from_the_end(head: Optional[ListNode], n: int):
    dummy = ListNode(0, head)

    prev = find_nth_from_end(dummy, n + 1)
    delete_after(prev)

    return dummy.next


def weave(a: Optional[ListNode], b: Optional[ListNode]):
    dummy = tail = ListNode()

    while a or b:
        if a:
            node, a = detach_front(a)
            tail = attach_after(tail, node)
        if b:
            node, b = detach_front(b)
            tail = attach_after(tail, node)

    return dummy.next


def merge(a: Optional[ListNode], b: Optional[ListNode]):
    dummy = tail = ListNode()

    while a and b:
        if a.val <= b.val:
            node, a = detach_front(a)
        else:
            node, b = detach_front(b)
        tail = attach_after(tail, node)

    tail.next = a or b

    return dummy.next


def sort(head: Optional[ListNode]):
    if not head or not head.next:
        return head

    left, right = split(head)

    return merge(
        sort(left),
        sort(right)
    )



def filter_list(head: Optional[ListNode], predicate):
    true_dummy, true_tail = ListNode()
    false_dummy, false_tail = ListNode()

    while head:
        node, head = detach_front(head)
        if predicate(node):
            true_tail = attach_after(true_tail, node)
        else:
            false_tail = attach_after(false_tail, node)

    return true_dummy.next, false_dummy.next





"""

Binary Tree

"""

class TreeNode:
    def __init__(self, val: int=0, left: Optional[TreeNode] = None, right: Optional[TreeNode] = None):
        self.val = val
        self.left = left
        self.right = right




