"""

Code Katha

"""


from __future__ import annotations

from collections import deque, defaultdict
from typing import Optional, Iterator, List

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

        return root

    return build(
        0,
        len(preorder),
        0,
        len(postorder)
    )

NULL = "#"
SEP = ","

def build_from_tokens(tokens: Iterator[str]) -> Optional[TreeNode]:
    token = next(tokens)

    if token == NULL:
        return None

    root = TreeNode(int(token))
    root.left = build_from_tokens(tokens)
    root.right = build_from_tokens(tokens)

    return root


def tree_to_tokens(root: Optional[TreeNode]) -> Iterator[str]:
    if not root:
        yield NULL
        return

    yield str(root.val)
    yield from tree_to_tokens(root.left)
    yield from tree_to_tokens(root.right)


def encode(tokens: Iterator[str]) -> str:
    return SEP.join(tokens)


def decode(data: str) -> Iterator[str]:
    return iter(data.split(sep=SEP))


def serialize(root: Optional[TreeNode]) -> str:
    return encode(tree_to_tokens(root))


def deserialize(data: str) -> Optional[TreeNode]:
    return build_from_tokens(decode(data))

"""

Binary Search Tree

"""

def is_leaf(node: Optional[TreeNode]) -> bool:
    return  (
        node is not None and
        node.left is None and
        node.right is None
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
    if not root: return None

    if key < root.val:
        return get(root.left, key)
    elif key == root.val:
        return root
    else:
        return get(root.right, key)


def contains(root: Optional[TreeNode], key: int) -> bool:
    return get(root, key) is not None


def put(root: Optional[TreeNode], key: int) -> Optional[TreeNode]:
    if not root: return TreeNode(key)

    if key < root.val:
        root.left = put(root.left, key)
    elif key > root.val:
        root.right = put(root.right, key)

    return update(root)


def rank(root: Optional[TreeNode], key: int) -> int:
    if not root: return 0

    if key < root.val:
        return rank(root.left, key)
    elif key == root.val:
        return size(root.left)
    else:
        return 1 + size(root.left) + rank(root.right, key)


def select(root: Optional[TreeNode], order: int) -> Optional[TreeNode]:
    if not root: return None

    left = root.left
    right = root.right

    if order < size(left):
        return select(left, order)
    elif order == size(left):
        return root
    else:
        return select(right, order - 1 - size(left))


def range_count(root: Optional[TreeNode], lo: int, hi: int) -> int:
    return rank(root, hi) - rank(root, lo) + int(contains(root, hi))


def range_nodes(root: Optional[TreeNode], lo: int, hi: int) -> Iterator[TreeNode]:
    if not root:
        return

    if lo < root.val:
        yield from range_nodes(root.left, lo, hi)
    if lo <= root.val <= hi:
        yield root
    if root.val < hi:
        yield from range_nodes(root.right, lo, hi)


def lca_bt(root: Optional[TreeNode], p: TreeNode, q: TreeNode) -> Optional[TreeNode]:
    if not root:
        return None

    if root is p or root is q:
        return root

    left = lca_bt(root.left, p, q)
    right = lca_bt(root.right, p, q)

    if left and right:
        return root

    return left or right


def lca_bt_non_guaranteed(root: Optional[TreeNode], p: TreeNode, q: TreeNode) -> Optional[TreeNode]:
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
    lo, hi = min(a, b), max(a, b)

    if not root:
        return None

    if lo > root.val:
        return lca_bst(root.right, lo, hi)
    elif hi < root.val:
        return lca_bst(root.left, lo, hi)
    else:
        return root


def lca_bst_non_guaranteed(root: Optional[TreeNode], a: int, b: int) -> Optional[TreeNode]:
    lo, hi = min(a, b), max(a, b)
    candidate = lca_bst(root, lo, hi)
    return candidate if contains(candidate, lo) and contains(candidate, hi) else None































