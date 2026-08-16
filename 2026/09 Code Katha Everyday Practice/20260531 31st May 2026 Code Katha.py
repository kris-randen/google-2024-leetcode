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


def list_nodes(a: Optional[ListNode]) -> Iterator[ListNode]:
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
    if not a or left >= right or left <= 0 or not has_k_nodes(a, left):
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
    if not a: return None, None

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
    if not root: return

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
    if not root: return

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
    if not root: return

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
    if not root: return

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
    if not root: return

    q = deque([(0, 0, 1, root.val, root)])
    while q:
        col, row, index, val, node = q.popleft()
        yield col, row, index, val, node

        if left := node.left:
            q.append((col - 1, row + 1, 2 * index, left.val, left))

        if right := node.right:
            q.append((col + 1, row + 1, 2 * index + 1, right.val, right))


def vertical_order(root: Optional[TreeNode]):
    cols = defaultdict(list)

    for col, row, index, val, node in level_order_pos(root):
        cols[col].append((col, row, index, val, node))

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

    return build(0, len(inorder))


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

    return build(0, len(inorder))


def build_from_pre_post(preorder: List[int], postorder: List[int]) -> Optional[TreeNode]:
    postorder_pos = {val: ind for ind, val in enumerate(postorder)}

    def size_left(pre_l, post_l):
        left_root_val = preorder[pre_l + 1]
        left_root_pos = postorder_pos[left_root_val]
        return left_root_pos - post_l + 1

    def build(
            pre_l: int,
            pre_r: int,
            post_l: int,
            post_r: int
    ):
        if pre_l >= pre_r:
            return None

        root_val = preorder[pre_l]
        root = TreeNode(root_val)
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


def lca_bt(root: Optional[TreeNode], p: TreeNode, q: TreeNode) -> Optional[TreeNode]:
    if not root: return None

    if root is p or root is q:
        return root

    left = lca_bt(root.left, p, q)
    right = lca_bt(root.right, p, q)

    if left and right:
        return root

    return left or right


def lca_bt_non_guaranteed(root: TreeNode, p: TreeNode, q: TreeNode) -> Optional[TreeNode]:
    def dfs(root: Optional[TreeNode]) -> tuple[Optional[TreeNode], bool, bool]:
        if not root:
            return None, False, False

        left_lca, left_has_p, left_has_q = dfs(root.left)
        right_lca, right_has_p, right_has_q = dfs(root.right)

        has_p = left_has_p or right_has_p or root is p
        has_q = left_has_q or right_has_q or root is q

        if left_lca:
            return left_lca, has_p, has_q

        if right_lca:
            return right_lca, has_p, has_q

        if has_p and has_q:
            return root, has_p, has_q

        return None, has_p, has_q

    lca, has_p, has_q = dfs(root)
    return lca if has_p and has_q else None


def lca_bst(root: Optional[TreeNode], a: int, b: int) -> Optional[TreeNode]:
    if not root:
        return None

    lo, hi = min(a, b), max(a, b)

    if lo > root.val:
        return lca_bst(root.right, a, b)
    elif hi < root.val:
        return lca_bst(root.left, a, b)
    else:
        return root


def lca_bst_non_guaranteed(root: TreeNode, a: int, b: int) -> Optional[TreeNode]:
    lo, hi = min(a, b), max(a, b)

    def dfs(root: Optional[TreeNode]):
        if not root:
            return None, False, False

        if lo > root.val:
            return dfs(root.right)
        elif hi < root.val:
            return dfs(root.left)
        else:
            left_lca, left_has_a, left_has_b = dfs(root.left)
            right_lca, right_has_a, right_has_b = dfs(root.right)

            has_a = left_has_a or right_has_a or root.val == a
            has_b = left_has_b or right_has_b or root.val == b

            if left_lca:
                return left_lca, has_a, has_b

            if right_lca:
                return right_lca, has_a, has_b

            if has_a and has_b:
                return root, has_a, has_b

            return None, has_a, has_b

    lca, has_a, has_b = dfs(root)
    return lca if has_a and has_b else None





