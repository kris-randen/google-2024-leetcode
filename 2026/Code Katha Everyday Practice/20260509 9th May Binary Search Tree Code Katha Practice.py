"""

Binary Search Tree

"""

from __future__ import annotations
from typing import Optional, Iterator, List


class TreeNode:
    def __init__(self, val: int = 0, left: Optional[TreeNode] = None, right: Optional[TreeNode] = None):
        self.val = val
        self.left = left
        self.right = right
        self.count = 1


def get(root: Optional[TreeNode], key: int):
    if root is None:
        return None

    if key < root.val:
        return get(root.left, key)
    if key > root.val:
        return get(root.right, key)

    return root


def put(root: Optional[TreeNode], key: int):
    if root is None:
        return TreeNode(key)

    if key < root.val:
        root.left = put(root.left, key)
    elif key > root.val:
        root.right = put(root.right, key)
    else:
        root.val = key

    root.count = 1 + size(root.left) + size(root.right)

    return root

def leftmost(root: TreeNode):
    while root.left:
        root = root.left
    return root

def rightmost(root: TreeNode):
    while root.right:
        root = root.right
    return root

def delete_min(root: TreeNode):
    if not root.left:
        return root.right

    root.left = delete_min(root.left)
    root.count = 1 + size(root.left) + size(root.right)
    return root


def delete(root: Optional[TreeNode], key: int):
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

    root.count = 1 + size(root.left) + size(root.right)
    return root


def size(root: Optional[TreeNode]):
    return root.count if root else 0


def height(root: Optional[TreeNode]):
    if not root:
        return 0

    return 1 + max(height(root.left), height(root.right))


def floor(root: Optional[TreeNode], key: int) -> Optional[TreeNode]:
    if not root:
        return None

    if key == root.val:
        return root
    if key < root.val:
        return floor(root.left, key)

    return floor(root.right, key) or root


def ceil(root: Optional[TreeNode], key: int) -> Optional[TreeNode]:
    if not root:
        return None

    if key > root.val:
        return ceil(root.right, key)
    if key == root.val:
        return root

    return ceil(root.left, key) or root

def rank(root: Optional[TreeNode], key: int) -> int:
    if not root:
        return 0

    if key < root.val:
        return rank(root.left, key)
    elif key == root.val:
        return size(root.left)
    else:
        return 1 + size(root.left) + rank(root.right)


def select(root: Optional[TreeNode], k: int) -> Optional[TreeNode]:
    if not root:
        return None

    if k < size(root.left):
        return select(root.left, k)
    elif k == size(root.left):
        return root
    else:
        return select(root.right, k - 1 - size(root.left))


def count(root: Optional[TreeNode], lo: int, hi: int) -> int:
    if not root:
        return 0

    return rank(root, hi + 1) - rank(root, lo)

def range(root: Optional[TreeNode], lo: int, hi: int) -> Iterator[TreeNode]:
    if not root:
        return

    if lo < root.val:
        yield from range(root.left, lo, hi)
    if lo <= root.val <= hi:
        yield root
    if root.val < hi:
        yield from range(root.right, lo, hi)

def inorder(root: Optional[TreeNode]) -> Iterator[TreeNode]:
    if not root:
        return

    yield from inorder(root.left)
    yield root
    yield from inorder(root.right)


def preorder(root: Optional[TreeNode]) -> Iterator[TreeNode]:
    if not root:
        return

    yield root
    yield from preorder(root.left)
    yield from preorder(root.right)


def postorder(root: Optional[TreeNode]) -> Iterator[TreeNode]:
    if not root:
        return

    yield from postorder(root.left)
    yield from postorder(root.right)
    yield root


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


