"""

Code Katha

"""

from __future__ import annotations
from collections import deque, defaultdict
from typing import List, Optional, Iterator, Iterable

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


def nodes_iter(a: Optional[ListNode]) -> Iterator[ListNode]:
    return iter(a) if a else iter(())


def values_iter(nodes: Iterable[ListNode]) -> Iterator[int]:
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
    if not target:
        return None

    prev.next = target.next
    target.next = None
    return target


def advance(a: Optional[ListNode], k: int) -> Optional[ListNode]:
    if k <= 0:
        return a

    for _ in range(k):
        if not a:
            break
        a = a.next

    return a


def has_k_nodes(a: Optional[ListNode], k: int) -> bool:
    return k <= 0 or advance(a, k - 1) is not None


def cycle_meet(a: Optional[ListNode]) -> Optional[ListNode]:
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
    if not meet:
        return None

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
    if not (left := a): return a, None

    mid = left_middle(left)
    right = cut_after(mid)
    return left, right


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
    if not a or not a.next:
        return a

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
    if not a or k <= 0:
        return None, None, a

    prev, tail, curr = None, a, a
    for _ in range(k):
        if not curr:
            break
        next = curr.next
        curr.next = prev
        prev = curr
        curr = next

    return prev, tail, curr


def reverse_between(a: Optional[ListNode], left: int, right: int) -> Optional[ListNode]:
    if not a or left >= right or left <= 0:
        return a

    dummy = ListNode(0, a)
    before = advance(dummy, left - 1)
    if not before or not before.next:
        return dummy.next

    start = before.next
    length = right - left + 1

    rhead, rtail, after = reverse_prefix(start, length)

    before.next = rhead
    rtail.next = after

    return dummy.next


def reverse_in_k_groups(a: Optional[ListNode], k: int) -> Optional[ListNode]:
    if not a or k <= 1:
        return a

    dummy = ListNode(0, a)
    before = dummy
    start = dummy.next

    while has_k_nodes(start, k):
        rhead, rtail, after = reverse_prefix(start, k)

        before.next = rhead
        rtail.next = after

        before = rtail
        start = before.next

    return dummy.next


"""

Binary Tree

"""


class TreeNode:
    def __init__(
            self,
            val: int = 0,
            left: Optional[TreeNode] = None,
            right: Optional[TreeNode] = None
    ):
        self.val = val
        self.left = left
        self.right = right
        self.count = 1
        self.height = 0


def size(node: Optional[TreeNode]) -> int:
    return node.count if node else 0


def height(node: Optional[TreeNode]) -> int:
    return node.height if node else -1


def update_size(node: Optional[TreeNode]):
    if not node: return
    node.count = 1 + size(node.left) + size(node.right)


def update_height(node: Optional[TreeNode]):
    if not node: return
    node.height = 1 + max(height(node.left), height(node.right))


def update(node: Optional[TreeNode]) -> Optional[TreeNode]:
    update_size(node)
    update_height(node)
    return node


Frame = tuple[Optional[TreeNode], bool]

def inorder_nodes(root: Optional[TreeNode]) -> Iterator[TreeNode]:
    if not root:
        return

    yield from inorder_nodes(root.left)
    yield root
    yield from inorder_nodes(root.right)


def inorder_iter(root: Optional[TreeNode]) -> Iterator[TreeNode]:
    stack: List[Frame] = [(root, False)]

    while stack:
        node, emit = stack.pop()

        if not node:
            continue

        if emit:
            yield node
        else:
            stack.append((node.right, False))
            stack.append((node, True))
            stack.append((node.left, False))


def preorder_nodes(root: Optional[TreeNode]) -> Iterator[TreeNode]:
    if not root:
        return

    yield root
    yield from preorder_nodes(root.left)
    yield from preorder_nodes(root.right)


def preorder_iter(root: Optional[TreeNode]) -> Iterator[TreeNode]:
    stack: List[Frame] = [(root, False)]

    while stack:
        node, emit = stack.pop()

        if not node:
            continue

        if emit:
            yield node
        else:
            stack.append((node.right, False))
            stack.append((node.left, False))
            stack.append((node, True))


def postorder_nodes(root: Optional[TreeNode]) -> Iterator[TreeNode]:
    if not root:
        return

    yield from postorder_nodes(root.left)
    yield from postorder_nodes(root.right)
    yield root








