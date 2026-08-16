"""

Code Katha

"""

from __future__ import annotations
from typing import Optional, Iterator, Iterable

"""

Binary Search Tree

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


def is_leaf(node: Optional[TreeNode]) -> bool:
    return (
        node is not None and
        node.left is None and
        node.right is None
    )


def is_left_child(node: Optional[TreeNode]) -> bool:
    return (
        node is not None and
        node.parent is not None and
        node is node.parent.left
    )


def is_right_child(node: Optional[TreeNode]) -> bool:
    return (
        node is not None and
        node.parent is not None and
        node is node.parent.right
    )


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


def leftmost(root: Optional[TreeNode]) -> Optional[TreeNode]:
    while root and root.left:
        root = root.left
    return root


def rightmost(root: Optional[TreeNode]) -> Optional[TreeNode]:
    while root and root.right:
        root = root.right
    return root


def get(root: Optional[TreeNode], key: int) -> Optional[TreeNode]:
    if not root:
        return None

    if key < root.val:
        return get(root.left, key)
    elif key > root.val:
        return get(root.right, key)
    else:
        return root


def contains(root: Optional[TreeNode], key: int) -> bool:
    return get(root, key) is not None


def put(root: Optional[TreeNode], key: int) -> Optional[TreeNode]:
    if not root:
        return TreeNode(key)

    if key < root.val:
        root.left = put(root.left, key)
    elif key > root.val:
        root.right = put(root.right, key)
    else:
        root.val = key

    return update(root)


def delete_min(root: Optional[TreeNode]) -> Optional[TreeNode]:
    if not root:
        return None

    if not root.left:
        return root.right

    root.left = delete_min(root.left)
    return update(root)


def delete_max(root: Optional[TreeNode]) -> Optional[TreeNode]:
    if not root:
        return None

    if not root.right:
        return root.left

    root.right = delete_max(root.right)
    return update(root)


def delete(root: Optional[TreeNode], key: int) -> Optional[TreeNode]:
    if not root:
        return None

    if key < root.val:
        root.left = delete(root.left, key)
    elif key > root.val:
        root.right = delete(root.right, key)
    else:
        if not root.left:
            return root.right
        if not root.right:
            return root.left

        successor = leftmost(root.right)
        successor.right = delete_min(root.right)
        successor.left = root.left
        root = successor

    return update(root)


def rank(root: Optional[TreeNode], key: int) -> int:
    if not root:
        return 0

    if key < root.val:
        return rank(root.left, key)
    elif key == root.val:
        return size(root.left)
    else:
        return 1 + size(root.left) + rank(root.right, key)


def select(root: Optional[TreeNode], order: int) -> Optional[TreeNode]:
    if not root:
        return None

    left, right = root.left, root.right

    if order < size(left):
        return select(left, order)
    elif order == size(left):
        return root
    else:
        return select(right, order - 1 - size(left))


def range_count(root: Optional[TreeNode], lo: int, hi: int) -> int:
    return rank(root, hi) - rank(root, lo) + int(contains(root, hi))


def floor(root: Optional[TreeNode], key: int) -> Optional[TreeNode]:
    if not root:
        return None

    if key < root.val:
        return floor(root.left, key)
    elif key == root.val:
        return root
    else:
        return floor(root.right, key) or root


def ceil(root: Optional[TreeNode], key: int) -> Optional[TreeNode]:
    if not root:
        return None

    if key > root.val:
        return ceil(root.right, key)
    elif key == root.val:
        return root
    else:
        return ceil(root.left, key) or root


def successor(p: TreeNode):
    if p.right:
        return leftmost(p.right)

    while is_right_child(p):
        p = p.parent

    return p.parent


def predecessor(p: TreeNode):
    if p.left:
        return rightmost(p.left)

    while is_left_child(p):
        p = p.parent

    return p.parent

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


def list_nodes(head: Optional[ListNode]) -> Iterator[ListNode]:
    return iter(head) if head else iter(())


def list_values(nodes: Iterable[ListNode]) -> Iterator[int]:
    return (node.val for node in nodes)


def detach_front(head: ListNode) -> tuple[ListNode, Optional[ListNode]]:
    rest = head.next
    head.next = None
    return head, rest


def attach_after(tail: ListNode, node: ListNode) -> ListNode:
    tail.next = node
    node.next = None
    return node


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


def advance(head: Optional[ListNode], k: int) -> Optional[ListNode]:
    if not head or k <= 0:
        return head

    for _ in range(k):
        if not head: break
        head = head.next

    return head


def has_k_nodes(head: Optional[ListNode], k: int) -> bool:
    return k <= 0 or advance(head, k - 1) is not None


def right_middle(head: Optional[ListNode]) -> Optional[ListNode]:
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    return slow


def left_middle(head: Optional[ListNode]) -> Optional[ListNode]:
    if not head:
        return head

    slow, fast = head, head.next
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    return slow


def split(head: Optional[ListNode]) -> tuple[Optional[ListNode], Optional[ListNode]]:
    if not (left := head):
        return None, None

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


def sort(head: Optional[ListNode]) -> Optional[ListNode]:
    if not head or not head.next:
        return head

    left, right = split(head)
    return merge(
        sort(left),
        sort(right)
    )


def remove_kth_from_end(head: Optional[ListNode], k: int) -> Optional[ListNode]:
    if not head or k <= 0 or not has_k_nodes(head, k):
        return head

    dummy = ListNode(0, head)
    slow = fast = dummy
    fast = advance(fast, k)

    while fast and fast.next:
        slow = slow.next
        fast = fast.next

    delete_after(slow)
    return dummy.next


def reverse(head: Optional[ListNode]) -> Optional[ListNode]:
    prev, curr = None, head
    while curr:
        next = curr.next
        curr.next = prev
        prev = curr
        curr = next
    return prev


def reverse_prefix(head: Optional[ListNode], k: int) -> tuple[Optional[ListNode], Optional[ListNode], Optional[ListNode]]:
    if not head or k <= 0:
        return None, None, head

    prev, tail, curr = None, head, head
    for _ in range(k):
        if not curr: break
        next = curr.next
        curr.next = prev
        prev = curr
        curr = next
    return prev, tail, curr


def reverse_between(head: Optional[ListNode], left: int, right: int) -> Optional[ListNode]:
    if not head or left >= right or left <= 0 or not has_k_nodes(head, left):
        return head

    dummy = ListNode(0, head)
    before = advance(dummy, left - 1)
    start = before.next
    length = right - left + 1

    rhead, rtail, after = reverse_prefix(start, length)
    before.next = rhead
    rtail.next = after
    return dummy.next


def reverse_in_k_groups(head: Optional[ListNode], k: int) -> Optional[ListNode]:
    if not head or k <= 1:
        return head

    dummy = ListNode(0, head)
    before = dummy
    start = before.next

    while has_k_nodes(start, k):
        rhead, rtail, after = reverse_prefix(start, k)

        before.next = rhead
        rtail.next = after

        before = rtail
        start = before.next

    return dummy.next


def cycle_meet(head: Optional[ListNode]) -> Optional[ListNode]:
    if not head or not head.next:
        return None

    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next

        if slow is fast:
            return slow

    return None


def has_cycle(head: Optional[ListNode]) -> bool:
    return cycle_meet(head) is not None


def cycle_start(head: Optional[ListNode]) -> Optional[ListNode]:
    meet = cycle_meet(head)
    if not meet:
        return None

    slow, fast = head, meet
    while slow is not fast:
        slow = slow.next
        fast = fast.next
    return slow



