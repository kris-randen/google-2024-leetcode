"""

Linked List

"""

from __future__ import annotations

from collections import deque, defaultdict
from typing import Optional, Iterator, Iterable, List


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

def detach_front(head: ListNode) -> tuple[ListNode, Optional[ListNode]]:
    rest = head.next
    head.next = None
    return head, rest

def attach_after(tail: ListNode, node: ListNode):
    tail.next = node
    node.next = None
    return node

def cut_after(prev: ListNode) -> Optional[ListNode]:
    rest = prev.next
    prev.next = None
    return rest

def delete_after(prev: ListNode) -> Optional[ListNode]:
    if not prev.next:
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
    slow = head
    fast = head

    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next

    return slow

def left_middle(head: Optional[ListNode]) -> Optional[ListNode]:
    if not head:
        return head

    slow = head
    fast = head.next

    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next

    return slow


def split(head: Optional[ListNode]) -> tuple[Optional[ListNode], Optional[ListNode]]:
    if not head:
        return head, None

    mid = left_middle(head)
    right = cut_after(mid)
    return head, right


def sort(head: Optional[ListNode]) -> Optional[ListNode]:
    if not head or not head.next:
        return head

    left, right = split(head)

    return merge(
        sort(left),
        sort(right)
    )


def advance(head: Optional[ListNode], k: int) -> Optional[ListNode]:
    if not head or k <= 0:
        return head

    for _ in range(k):
        if not head:
            break
        head = head.next

    return head

def has_k_nodes(head: Optional[ListNode], k: int) -> bool:
    if k <= 0:
        return True

    dummy = ListNode(0, head)
    return advance(dummy, k) is not None

def reverse(head: Optional[ListNode]) -> Optional[ListNode]:
    if not head:
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
    if not head or k <= 0:
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

def reverse_between(head: Optional[ListNode], left: int, right: int) -> Optional[ListNode]:
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


def reverse_in_k_groups(head: Optional[ListNode], k: int) -> Optional[ListNode]:
    if not head or k <= 1:
        return head

    dummy = ListNode(0, head)
    prev_group = dummy
    start = prev_group.next

    while has_k_nodes(start, k):
        rev_head, rev_tail, after = reverse_prefix(start, k)

        prev_group.next = rev_head
        rev_tail.next = after

        prev_group = rev_tail
        start = prev_group.next

    return dummy.next


def has_cycle(head: Optional[ListNode]) -> Optional[ListNode]:
    slow = head
    fast = head

    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next

        if slow is fast:
            return slow

    return None

def cycle_start(head: Optional[ListNode]) -> Optional[ListNode]:
    meet = has_cycle(head)

    if not meet:
        return None

    slow = head
    fast = meet

    while slow is not fast:
        slow = slow.next
        fast = fast.next

    return slow

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


def is_leaf(node: Optional[TreeNode]) -> bool:
    return (
        node is not None and
        node.left is None and
        node.right is None
    )


def inorder_nodes(root: Optional[TreeNode]) -> Iterator[TreeNode]:
    if not root:
        return

    yield from inorder_nodes(root.left)
    yield root
    yield from inorder_nodes(root.right)


Frame = tuple[Optional[TreeNode], bool]

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


def postorder_iter(root: Optional[TreeNode]) -> Iterator[TreeNode]:
    stack: List[Frame] = [(root, False)]

    while stack:
        node, emit = stack.pop()

        if not node:
            continue

        if emit:
            yield node
        else:
            stack.append((node, True))
            stack.append((node.right, False))
            stack.append((node.left, False))


def level_order(root: Optional[TreeNode]) -> Iterator[List[TreeNode]]:
    if not root:
        return

    q = deque([root])
    while q:
        level, level_size = [], len(q)
        for _ in range(level_size):
            node = q.popleft()
            level.append(node)

            if node.left:
                q.append(node.left)
            if node.right:
                q.append(node.right)

        yield level

def level_order_pos(root: Optional[TreeNode]):
    if not root:
        return

    q = deque([(0, 0, root.val, 1, root)])
    while q:
        col, row, val, index, node = q.popleft()
        yield col, row, val, index, node

        if node.left:
            q.append((col - 1, row + 1, node.left.val, 2 * index, node.left))
        if node.right:
            q.append((col + 1, row + 1, node.right.val, 2 * index + 1, node.right))

def vertical_order(root: Optional[TreeNode]):
    cols = defaultdict(list)

    for col, row, val, _, _ in level_order_pos(root):
        cols[col].append((col, row, val))

    return [sorted(cols[c]) for c in sorted(cols)]


def build_from_pre_in(preorder: List[int], inorder: List[int]) -> Optional[TreeNode]:
    inorder_pos = {val: ind for ind, val in enumerate(inorder)}
    ind = 0

    def build(start, end) -> Optional[TreeNode]:
        nonlocal ind

        if start >= end:
            return None

        val = preorder[ind]
        root = TreeNode(val)
        ind += 1

        mid = inorder_pos[val]
        root.left = build(start, mid)
        root.right = build(mid + 1, end)

        return root

    return build(0, len(preorder))


def build_from_in_post(inorder: List[int], postorder: List[int]) -> Optional[TreeNode]:
    inorder_pos = {val: ind for ind, val in enumerate(inorder)}
    ind = len(postorder) - 1

    def build(start, end) -> Optional[TreeNode]:
        nonlocal ind

        if start >= end:
            return None

        val = postorder[ind]
        root = TreeNode(val)
        ind -= 1

        mid = inorder_pos[val]
        root.right = build(mid + 1, end)
        root.left = build(start, mid)

        return root

    return build(0, len(postorder))


def build_from_pre_post(preorder: List[int], postorder: List[int]) -> Optional[TreeNode]:
    post_pos = {val: ind for ind, val in enumerate(postorder)}

    def left_size(pre_l, post_l):
        left_root_val = preorder[pre_l + 1]
        left_root_pos = post_pos[left_root_val]
        return left_root_pos - post_l + 1

    def build(
            pre_l,
            pre_r,
            post_l,
            post_r
    ):
        if pre_l >= pre_r:
            return None

        root_val = preorder[pre_l]
        root = TreeNode(root_val)
        if pre_r - pre_l == 1:
            return root

        size_left = left_size(pre_l, post_l)
        root.left = build(
            pre_l + 1,
            pre_l + 1 + size_left,
            post_l,
            post_l + size_left
        )
        root.right = build(
            pre_l + 1 + size_left,
            pre_r,
            post_l + size_left,
            post_r - 1
        )

        return root

    return build(0, len(preorder), 0, len(postorder))



"""

Binary Search Tree

"""


def size(node: Optional[TreeNode]) -> int:
    return node.count if node else 0

def height(node: Optional[TreeNode]) -> int:
    return node.height if node else -1

def update_size(node: Optional[TreeNode]) -> None:
    if not node: return
    node.count = 1 + size(node.left) + size(node.right)

def update_height(node: Optional[TreeNode]) -> None:
    if not node: return
    node.height = 1 + max(height(node.left), height(node.right))

def update(node: Optional[TreeNode]) -> Optional[TreeNode]:
    update_size(node)
    update_height(node)
    return node

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

def leftmost(root: Optional[TreeNode]) -> Optional[TreeNode]:
    while root and root.left:
        root = root.left
    return root

def rightmost(root: Optional[TreeNode]) -> Optional[TreeNode]:
    while root and root.right:
        root = root.right
    return root

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
        elif not root.right:
            return root.left
        else:
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
    elif key > root.val:
        return 1 + size(root.left) + rank(root.right, key)
    else:
        return size(root.left)

def select(root: Optional[TreeNode], order: int) -> Optional[TreeNode]:
    if not root:
        return None

    if order == size(root.left):
        return root
    elif order < size(root.left):
        return select(root.left, order)
    else:
        return select(root.right, order - 1 - size(root.left))


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

def count(root: Optional[TreeNode], lo: int, hi: int) -> int:
    if not root or lo > hi:
        return 0
    return rank(root, hi) - rank(root, lo) + int(contains(root, hi))

def range_nodes(root: Optional[TreeNode], lo: int, hi: int) -> Iterator[TreeNode]:
    if not root:
        return

    if lo < root.val:
        yield from range_nodes(root.left, lo, hi)
    if lo <= root.val <= hi:
        yield root
    if hi > root.val:
        yield from range_nodes(root.right, lo, hi)



