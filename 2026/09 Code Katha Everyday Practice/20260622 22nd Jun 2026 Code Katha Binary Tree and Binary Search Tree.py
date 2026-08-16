"""

Code Katha

"""


from __future__ import annotations
from collections import deque, defaultdict
from typing import Optional, Iterator, Iterable, List


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
    return(
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
        return update(root)

    build(
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
    elif key == root.val:
        return root
    else:
        return get(root.right, key)


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


def pred(root: Optional[TreeNode], key: int) -> Optional[TreeNode]:
    if not root:
        return None

    if key <= root.val:
        return pred(root.left, key)
    else:
        return pred(root.right, key) or root


def succ(root: Optional[TreeNode], key: int) -> Optional[TreeNode]:
    if not root:
        return None

    if key >= root.val:
        return succ(root.right, key)
    else:
        return succ(root.left, key) or root


def predecessor(p: TreeNode) -> Optional[TreeNode]:
    if p.left:
        return rightmost(p.left)

    while is_left_child(p):
        p = p.parent

    return p.parent


def successor(p: TreeNode) -> Optional[TreeNode]:
    if p.right:
        return leftmost(p.right)

    while is_right_child(p):
        p = p.parent

    return p.parent



























