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


def right_middle(x: Optional[ListNode]) -> Optional[ListNode]:
    slow = fast = x
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    return slow


def left_middle(x: Optional[ListNode]) -> Optional[ListNode]:
    if not x:
        return None

    slow, fast = x, x.next
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    return slow


def split(x: Optional[ListNode]) -> tuple[Optional[ListNode], Optional[ListNode]]:
    if not (left := x):
        return None, None

    mid = left_middle(left)
    right = cut_after(mid)
    return left, right


def cycle_meet(x: Optional[ListNode]) -> Optional[ListNode]:
    if not x:
        return None

    slow = fast = x
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next

        if slow is fast:
            return slow

    return None


def has_cycle(x: Optional[ListNode]) -> bool:
    return cycle_meet(x) is not None


def cycle_start(x: Optional[ListNode]) -> Optional[ListNode]:
    meet = cycle_meet(x)
    if not meet:
        return None

    slow, fast = x, meet
    while slow is not fast:
        slow = slow.next
        fast = fast.next
    return slow


def reverse(x: Optional[ListNode]) -> Optional[ListNode]:
    prev, curr = None, x
    while curr:
        next = curr.next
        curr.next = prev
        prev = curr
        curr = next
    return prev


def reverse_prefix(x: Optional[ListNode], k: int) -> \
    tuple[Optional[ListNode], Optional[ListNode], Optional[ListNode]]:
    if not x or k <= 0:
        return None, None, x

    prev, tail, curr = None, x, x
    for _ in range(k):
        if not curr: break
        next = curr.next
        curr.next = prev
        prev = curr
        curr = next
    return prev, tail, curr


def reverse_between(x: Optional[ListNode], left: int, right: int) -> Optional[ListNode]:
    if not x or left >= right or left <= 0 or not has_k_nodes(x, left):
        return x

    dummy = ListNode(0, x)
    before = advance(dummy, left - 1)
    start = before.next
    length = right - left + 1

    if not has_k_nodes(start, length):
        return dummy.next

    rhead, rtail, after = reverse_prefix(start, length)
    before.next = rhead
    rtail.next = after
    return dummy.next


def reverse_in_k_groups(x: Optional[ListNode], k: int) -> Optional[ListNode]:
    if not x or k <= 1:
        return x

    dummy = ListNode(0, x)
    before = dummy
    start = before.next

    while has_k_nodes(start, k):
        rhead, rtail, after = reverse_prefix(start, k)

        before.next = rhead
        rtail.next = after

        before = rtail
        start = before.next

    return dummy.next


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


def sort_list(x: Optional[ListNode]) -> Optional[ListNode]:
    if not x or not x.next:
        return x

    left, right = split(x)
    return merge(
        sort_list(left),
        sort_list(right)
    )


def remove_kth_from_end(x: Optional[ListNode], k: int) -> Optional[ListNode]:
    if not x or k <= 0 or not has_k_nodes(x, k):
        return x

    dummy = ListNode(0, x)
    slow = fast = dummy
    fast = advance(fast, k)

    while fast and fast.next:
        slow = slow.next
        fast = fast.next

    delete_after(slow)
    return dummy.next


"""

Binary Tree

"""


class TreeNode:
    def __init__(
            self,
            val: int = 0,
            left: Optional[TreeNode] = None,
            right: Optional[TreeNode] = None,
            parent: Optional[TreeNode] = None
    ):
        self.val = val
        self.left = left
        self.right = right
        self.parent = parent
        self.count = 1
        self.height = 0


def is_leaf(x: Optional[TreeNode]) -> bool:
    return (
        x is not None and
        x.left is None and
        x.right is None
    )


def is_left_child(x: Optional[TreeNode]) -> bool:
    return (
        x is not None and
        x.parent is not None and
        x is x.parent.left
    )


def is_right_child(x: Optional[TreeNode]) -> bool:
    return (
        x is not None and
        x.parent is not None and
        x is x.parent.right
    )


def size(x: Optional[TreeNode]) -> int:
    return x.count if x else 0


def height(x: Optional[TreeNode]) -> int:
    return x.height if x else -1


def update_size(x: Optional[TreeNode]):
    if not x: return
    x.count = 1 + size(x.left) + size(x.right)


def update_height(x: Optional[TreeNode]):
    if not x: return
    x.height = 1 + max


def buildsubseqences(s):
    if len(s) == 0:
        return set()

    if len(s) == 1:
        return {"s", ""}

    u = s[0]
    without_u = buildsubseqences(s[1:])
    with_u = set([u + ss for ss in without_u])
    return with_u.union(without_u)










