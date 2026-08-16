"""

Code Katha

"""


from __future__ import annotations

from collections import deque, defaultdict
from encodings.rot_13 import rot13
from plistlib import dump
from typing import Optional, Iterator, Iterable, List

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
    x.height = 1 + max(height(x.left), height(x.right))


def update(x: Optional[TreeNode]) -> Optional[TreeNode]:
    update_size(x)
    update_height(x)
    return x


def inorder_nodes(root: Optional[TreeNode]) -> Iterator[TreeNode]:
    if not root: return

    yield from inorder_nodes(root.left)
    yield root
    yield from inorder_nodes(root.right)


def inorder_iter(root: Optional[TreeNode]) -> Iterator[TreeNode]:
    stack = [(root, False)]

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
    stack = [(root, False)]

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
    stack = [(root, False)]

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


def level_order_pos(root: Optional[TreeNode]) -> Iterator[tuple[int, int, int, int, TreeNode]]:
    if not root: return

    q = deque([(0, 0, 1, root.val, root)])
    while q:
        col, row, index, val, node = q.popleft()
        yield col, row, index, val, node

        if left := node.left:
            q.append((col - 1, row + 1, 2 * index, left.val, left))

        if right := node.right:
            q.append((col + 1, row + 1, 2 * index + 1, right.val, right))


def vertical_order(root: Optional[TreeNode]) -> List[List[tuple[int, int, int, int, TreeNode]]]:
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

        return update(root)

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

        return update(root)

    return build(0, len(inorder))


def build_from_pre_post(preorder: List[int], postorder: List[int]) -> Optional[TreeNode]:
    postorder_pos = {val: ind for ind, val in enumerate(postorder)}

    def size_left(pre_l: int, post_l: int) -> int:
        left_root_val = preorder[pre_l + 1]
        left_root_pos = postorder_pos[left_root_val]
        return left_root_pos - post_l + 1

    def build(
            pre_l: int,
            pre_r: int,
            post_l: int,
            post_r: int
    ) -> Optional[TreeNode]:
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
        return update(root)

    return build(
        0,
        len(preorder),
        0,
        len(postorder)
    )


NULL, SEP = '#', ','


def build_from_tokens(tokens: Iterator[str]) -> Optional[TreeNode]:
    token = next(tokens)

    if token == NULL:
        return None

    root = TreeNode(int(token))
    root.left = build_from_tokens(tokens)
    root.right = build_from_tokens(tokens)
    return update(root)


def tree_to_tokens(root: Optional[TreeNode]) -> Iterator[str]:
    pass



















