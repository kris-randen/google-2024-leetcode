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


def nodes(head: Optional[ListNode]) -> Iterator[ListNode]:
    return iter(head) if head else iter(())

def values(ns: Iterable[ListNode]) -> Iterator[int]:
    return (node.val for node in ns)

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
    if not prev.next:
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
    if not (left := head):
        return None, None

    mid = left_middle(head)
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

def advance(head: Optional[ListNode], k: int) -> Optional[ListNode]:
    if not (curr := head) or k <= 0:
        return head

    for _ in range(k):
        if not curr:
            break
        curr = curr.next

    return curr


def has_k_nodes(head: Optional[ListNode], k: int) -> bool:
    if k <= 0:
        return True

    return advance(head, k - 1) is not None


def reverse(head: Optional[ListNode]) -> Optional[ListNode]:
    if not head or not head.next:
        return head

    prev, curr = None, head

    while curr:
        next = curr.next
        curr.next = prev
        prev = curr
        curr = next

    return prev

def reverse_prefix(head: Optional[ListNode], k: int) -> \
    tuple[Optional[ListNode], Optional[ListNode], Optional[ListNode]]:
    if not head or k <= 0 or not has_k_nodes(head, k):
        return None, None, head

    prev, curr, tail = None, head, head

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

    rhead, rtail, after = reverse_prefix(start, length)

    before.next = rhead
    rtail.next = after

    return dummy.next


def reverse_in_k_groups(head: Optional[ListNode], k: int) -> Optional[ListNode]:
    if not head or k <= 1:
        return head

    dummy = ListNode(0, head)
    prev_group = dummy
    start = prev_group.next

    while has_k_nodes(start, k):
        rhead, rtail, after = reverse_prefix(start, k)

        prev_group.next = rhead
        rtail.next = after

        prev_group = rtail
        start = prev_group.next

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


def is_leaf(node: Optional[TreeNode]) -> bool:
    return (
        node is not None and
        node.left is None and
        node.right is None
    )

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


def level_order(root: TreeNode) -> Iterator[List[TreeNode]]:
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

def level_order_pos(root: TreeNode) -> tuple[int, int, int, int, TreeNode]:
    q = deque([(0, 0, root.val, 1, root)])

    while q:
        col, row, val, index, node = q.popleft()

        yield col, row, val, index, node
        if left := node.left:
            q.append((col - 1, row + 1, left.val, 2 * index, left))
        if right := node.right:
            q.append((col + 1, row + 1, right.val, 2 * index + 1, right))

def vertical_order(root: TreeNode) -> List[List[tuple[int, int, int]]]:
    cols = defaultdict(list)

    for col, row, val, _, _ in level_order_pos(root):
        cols[col].append((col, row, val))

    return [sorted(cols[c]) for c in sorted(cols)]


def build_from_pre_in(preorder: List[int], inorder: List[int]) -> Optional[TreeNode]:
    inorder_pos = {val: ind for ind, val in enumerate(inorder)}
    ind = 0

    def build(start: int, end: int) -> Optional[TreeNode]:
        nonlocal ind

        if start >= end:
            return None

        val = preorder[ind]
        mid = inorder_pos[val]
        ind += 1

        root = TreeNode(val)
        root.left = build(start, mid)
        root.right = build(mid + 1, end)

        return root

    return build(0, len(preorder))


def build_from_in_post(inorder: List[int], postorder: List[int]) -> Optional[TreeNode]:
    inorder_pos = {val: ind for ind, val in enumerate(inorder)}
    ind = len(postorder) - 1

    def build(start: int, end: int) -> Optional[TreeNode]:
        nonlocal ind

        if start >= end:
            return None

        val = postorder[ind]
        mid = inorder_pos[val]
        ind -= 1

        root = TreeNode(val)
        root.right = build(mid + 1, end)
        root.left = build(start, mid)

        return root

    return build(0, len(postorder))


def build_from_pre_post(preorder: List[int], postorder: List[int]) -> Optional[TreeNode]:
    post_pos = {val: ind for ind, val in enumerate(postorder)}

    def size_left(pre_l, post_l):
        left_root_val = preorder[pre_l + 1]
        left_root_pos = post_pos[left_root_val]
        return left_root_pos - post_l + 1

    def build(
            pre_l: int,
            pre_r: int,
            post_l: int,
            post_r: int
    ):
        if pre_l >= pre_r:
            return None

        val = preorder[pre_l]
        root = TreeNode(val)
        if pre_r - pre_l == 1:
            return root

        left_size = size_left(pre_l, post_l)
        root.left = build(
            pre_l + 1,
            pre_l + 1 + left_size,
            post_l,
            post_l + left_size
        )
        root.right = build(
            pre_l + 1 + left_size,
            pre_r,
            post_l + left_size,
            post_r - 1
        )

        return root

    return build(0, len(preorder), 0, len(postorder))


def lca(root: Optional[TreeNode], p: TreeNode, q: TreeNode) -> Optional[TreeNode]:
    if not root:
        return None

    if root is p or root is q:
        return root

    left = lca(root.left, p, q)
    right = lca(root.right, p, q)

    if left and right:
        return root

    return left or right


def lca_non_guaranteed(root: Optional[TreeNode], p: TreeNode, q: TreeNode) -> Optional[TreeNode]:
    def dfs(node: Optional[TreeNode]) -> tuple[Optional[TreeNode], bool, bool]:
        if not node:
            return None, False, False

        left_lca, left_has_p, left_has_q = dfs(node.left)
        right_lca, right_has_p, right_has_q = dfs(node.right)

        has_p = left_has_p or right_has_p or node is p
        has_q = left_has_q or right_has_q or node is q

        if left_lca:
            return left_lca, has_p, has_q

        if right_lca:
            return right_lca, has_p, has_q

        if has_p and has_q:
            return node, has_p, has_q

        return None, has_p, has_q

    lca, _, _ = dfs(root)
    return lca




"""

Binary Search Tree

"""


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


def size(node: Optional[TreeNode]) -> int:
    return node.count if node else 0

def height(node: Optional[TreeNode]) -> int:
    return node.height if node else -1

def update_size(node: TreeNode):
    node.count = 1 + size(node.left) + size(node.right)

def update_height(node: TreeNode):
    node.height = 1 + max(height(node.left), height(node.right))

def update(node: TreeNode) -> TreeNode:
    update_size(node)
    update_height(node)
    return node

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

def rank(root: Optional[TreeNode], key: int) -> int:
    if not root:
        return 0

    left, right = root.left, root.right

    if key < root.val:
        return rank(left, key)
    elif key == root.val:
        return size(left)
    else:
        return 1 + size(left) + rank(right, key)

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

def count(root: Optional[TreeNode], lo: int, hi: int) -> int:
    return rank(root, hi) - rank(root, lo) + int(contains(root, hi))

def range_iter(root: Optional[TreeNode], lo: int, hi: int) -> Iterator[TreeNode]:
    if not root:
        return

    if lo < root.val:
        yield from range_iter(root.left, lo, hi)
    if lo <= root.val <= hi:
        yield root
    if root.val < hi:
        yield from range_iter(root.right, lo, hi)

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
        if not root.right:
            return root.left
        successor = leftmost(root.right)
        successor.right = delete_min(root.right)
        successor.left = root.left
        root = successor

    return update(root)









def lca_bst(root: Optional[TreeNode], p: TreeNode, q: TreeNode) -> Optional[TreeNode]:
    lo, hi = min(p.val, q.val), max(p.val, q.val)

    def rec(root: Optional[TreeNode]) -> Optional[TreeNode]:
        if not root:
            return None

        if hi < root.val:
            return rec(root.left)
        elif lo > root.val:
            return rec(root.right)
        else:
            return root

    return rec(root)


def lca_bst_non_guaranteed(root: TreeNode, p: TreeNode, q: TreeNode) -> Optional[TreeNode]:
    lo, hi = min(p.val, q.val), max(p.val, q.val)

    def dfs(node: Optional[TreeNode]):
        if not node:
            return None, False, False

        if hi < node.val:
            return dfs(node.left)
        elif lo > node.val:
            return dfs(node.right)
        else:
            left_lca, left_has_p, left_has_q = dfs(node.left)
            right_lca, right_has_p, right_has_q = dfs(node.right)

            has_p = left_has_p or right_has_p or node is p
            has_q = left_has_q or right_has_q or node is q

            if left_lca:
                return left_lca, has_p, has_q
            if right_lca:
                return right_lca, has_p, has_q
            if has_p and has_q:
                return node, has_p, has_q

            return None, has_p, has_q

    lca, _, _ = dfs(root)
    return lca

