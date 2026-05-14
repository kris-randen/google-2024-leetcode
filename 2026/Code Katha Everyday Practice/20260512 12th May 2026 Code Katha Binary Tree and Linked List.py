"""

Code Katha

"""

from __future__ import annotations

from collections import deque, defaultdict
from typing import Optional, Iterator, List

"""

Dynamic Programming

"""

# Longest Palindromic Substring

def pad(s: str) -> str:
    return "#" + "#".join(s) + "#"

def expand(t: str, center: int):
    l, r, n = center, center, len(t)

    while l >= 0 and r < n and t[l] == t[r]:
        l -= 1
        r += 1

    return l + 1, r - 1

def longest_palindrome(s: str) -> str:
    t, best = pad(s), (0, 0)

    for center in range_tree(len(t)):
        l, r = expand(t, center)

        if r - l > best[1] - best[0]:
            best = l, r

    return t[best[0]:best[1] + 1].replace("#", "")

"""

Binary Search Tree

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

def size(root: Optional[TreeNode]) -> int:
    return 0 if not root else root.count

def height(root: Optional[TreeNode]) -> int:
    return -1 if not root else root.height

def update_size(root: TreeNode):
    root.count = 1 + size(root.left) + size(root.right)

def update_height(root: TreeNode):
    root.height = 1 + max(height(root.left), height(root.right))

def update(root: TreeNode):
    update_size(root)
    update_height(root)
    return root

def is_leaf(node: Optional[TreeNode]):
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

def preorder_nodes(root: Optional[TreeNode]) -> Iterator[TreeNode]:
    if not root:
        return

    yield root
    yield from preorder_nodes(root.left)
    yield from preorder_nodes(root.right)

def postorder_nodes(root: Optional[TreeNode]) -> Iterator[TreeNode]:
    if not root:
        return

    yield from postorder_nodes(root.left)
    yield from postorder_nodes(root.right)
    yield root


Frame = tuple[Optional[TreeNode], bool]

def inorder_iter(root: Optional[TreeNode]) -> Iterator[TreeNode]:
    stack: List[Frame] = [(root, False)] if root else []

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

def preorder_iter(root: Optional[TreeNode]) -> Iterator[TreeNode]:
    stack: List[Frame] = [(root, False)] if root else []

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

def postorder_iter(root: Optional[TreeNode]) -> Iterator[TreeNode]:
    stack: List[Frame] = [(root, False)] if root else []

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
        if not root.right:
            return root.left

        t = leftmost(root.right)
        t.right = delete_min(root.right)
        t.left = root.left
        root = t

    return update(root)

def rank(root: Optional[TreeNode], key: int) -> int:
    if not root:
        return 0

    if key == root.val:
        return size(root.left)
    elif key < root.val:
        return rank(root.left, key)
    else:
        return 1 + size(root.left) + rank(root.right, key)

def select(root: Optional[TreeNode], order: int) -> Optional[TreeNode]:
    if not root:
        return None

    if order == size(root.left):
        return root
    elif order < size(root.left):
        return select(root.left, order)
    else:
        return select(root.right, order - 1 - size(root.left))

def count(root: Optional[TreeNode], lo: int, hi: int) -> int:
    if not root:
        return 0
    return (
        rank(root, hi) -
        rank(root, lo) +
        int(contains(root, hi))
    )

def range_tree(root: Optional[TreeNode], lo: int, hi: int) -> Iterator[TreeNode]:
    if not root:
        return

    if lo < root.val:
        yield from range_tree(root.left, lo, hi)
    if lo <= root.val <= hi:
        yield root
    if hi > root.val:
        yield from range_tree(root.right, lo, hi)



"""

Binary Tree

"""

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

    q = deque([(0, 0, root.val, 1, root)]) # col, row, val, index

    while q:
        col, row, val, index, node = q.popleft()

        yield col, row, val, index, node

        if node.left:
            q.append((col - 1, row + 1, node.left.val, 2 * index, node.left))
        if node.right:
            q.append((col + 1 , row + 1, node.right.val, 2 * index + 1, node.right))


def vertical_order(root: Optional[TreeNode]):
    cols = defaultdict(list)

    for col, row, val, _, _ in level_order_pos(root):
        cols[col].append((col, row, val))

    return [sorted(cols[c]) for c in sorted(cols)]



def build_from_pre_in(preorder: List[int], inorder: List[int]) -> Optional[TreeNode]:
    if not inorder:
        return None

    inorder_pos = {val: ind for ind, val in enumerate(inorder)}
    ind = 0

    def build(start: int, end: int):
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
    if not inorder:
        return None

    inorder_pos = {val: ind for ind, val in enumerate(inorder)}
    ind = len(inorder) - 1

    def build(start: int, end: int):
        nonlocal  ind

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



def build_from_pre_post(
        preorder: List[int],
        postorder: List[int]
) -> Optional[TreeNode]:
    if not preorder:
        return None

    post_pos_ind = {val: ind for ind, val in enumerate(postorder)}

    def size_left(pre_l, post_l):
        left_root = preorder[pre_l + 1]
        left_root_pos = post_pos_ind[left_root]
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

        lsize = size_left(pre_l, post_l)
        root.left = build(
            pre_l + 1,
            pre_l + 1 + lsize,
            post_l,
            post_l + lsize
        )
        root.right = build(
            pre_l + 1 + lsize,
            pre_r,
            post_l + lsize,
            post_r - 1
        )

        return update(root)

    return build(0, len(preorder), 0, len(postorder))



def build_from_pre_pos(preorder: List[int], postorder: List[int]) -> Optional[TreeNode]:
    if not preorder:
        return None

    post_pos = {val: ind for ind, val in enumerate(postorder)}

    def size_left(pre_l, post_l):
        left_root = preorder[pre_l + 1]
        left_root_pos = post_pos[left_root]
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

        l_size = size_left(pre_l, post_l)

        root.left = build(
            pre_l + 1,
            pre_l + 1 + l_size,
            post_l,
            post_l + l_size
        )
        root.right = build(
            pre_l + 1 + l_size,
            pre_r,
            post_l + l_size,
            post_r - 1
        )

        return update(root)

    return build(
        0,
        len(preorder),
        0,
        len(postorder)
    )


