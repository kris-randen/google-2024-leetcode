"""

Binary Search Tree

"""

from __future__ import annotations

from typing import Optional, Iterator, List


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

def is_leaf(root: Optional[TreeNode]) -> bool:
    return (
        root is not None and
        root.left is None and
        root.right is None
    )

def size(root: Optional[TreeNode]) -> int:
    return root.count if root else 0

def height(root: Optional[TreeNode]) -> int:
    return root.height if root else -1

def update_size(root: Optional[TreeNode]):
    if not root:
        return

    root.count = 1 + size(root.left) + size(root.right)

def update_height(root: Optional[TreeNode]):
    if not root:
        return

    root.height = 1 + max(height(root.left), height(root.right))

def update(root: Optional[TreeNode]) -> Optional[TreeNode]:
    if not root:
        return None

    update_size(root)
    update_height(root)

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

def put(root: Optional[TreeNode], key: int) -> Optional[TreeNode]:
    if not root:
        return TreeNode(val=key)

    if key < root.val:
        root.left = put(root.left, key)
    elif key > root.val:
        root.right = put(root.right, key)
    else:
        return root

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


def select(root: Optional[TreeNode], index: int) -> Optional[TreeNode]:
    if not root or index < 0 or index >= size(root):
        return None

    if index < size(root.left):
        return select(root.left, index)
    elif index == size(root.left):
        return root
    else:
        return select(root.right, index - (1 + size(root.left)))


def floor(root: Optional[TreeNode], key: int) -> Optional[TreeNode]:
    if not root:
        return None

    if key < root.val:
        return floor(root.left, key)
    elif key == root.val:
        return root
    else:
        return floor(root.right, key) or root

def is_left_child(node: TreeNode) -> bool:
    if not node.parent:
        return False
    return node.parent.left is node

def is_right_child(node: TreeNode) -> bool:
    if not node.parent:
        return False
    return node.parent.right is node

def predecessor(node: TreeNode) -> Optional[TreeNode]:
    if node.left:
        return rightmost(node.left)

    while is_left_child(node) and node.parent:
        node = node.parent

    return node.parent

def successor(node: TreeNode) -> Optional[TreeNode]:
    if node.right:
        return leftmost(node.right)

    while is_right_child(node) and node.parent:
        node = node.parent

    return node.parent

def contains(root: Optional[TreeNode], key: int) -> bool:
    return get(root, key) is not None


def range_count(root: Optional[TreeNode], lo: int, hi: int) -> int:
    if not root:
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


def lowest_common_ancestor(root: Optional[TreeNode], p: TreeNode, q: TreeNode):
    lo, hi = min(p.val, q.val), max(p.val, q.val)

    while root:
        if hi < root.val:
            root = root.left
        elif lo > root.val:
            root = root.right
        else:
            return root

    return None

"""

Binary Tree

"""


