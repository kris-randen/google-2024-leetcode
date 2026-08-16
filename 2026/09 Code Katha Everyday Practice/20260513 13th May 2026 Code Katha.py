"""

Binary Tree

"""

from __future__ import annotations

from collections import deque, defaultdict
from typing import Optional, Iterator, List


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
    if not root:
        return

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
    if not root:
        return

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
    if not root:
        return

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


def level_order_pos(root: Optional[TreeNode]) -> Iterator[TreeNode]:
    if not root:
        return

    q = deque([(0, 0, root.val, 1, root)])

    while q:
        col, row, val, index, node = q.popleft()
        yield col, row, val, index, node

        if left := node.left:
            q.append((col - 1, row + 1, left.val, 2 * index, left))
        if right := node.right:
            q.append((col + 1, row + 1, right.val, 2 * index + 1, right))


def vertical_order(root: Optional[TreeNode]):
    if not root:
        return []

    cols = defaultdict(list)

    for col, row, val, index, node in level_order_pos(root):
        cols[col].append((col, row, val, index, node))

    return [sorted(cols[c]) for c in sorted(cols)]

def build_from_pre_in(preorder: List[int], inorder: List[int]) -> Optional[TreeNode]:
    inorder_pos = {val: ind for ind, val in enumerate(inorder)}
    ind = 0

    def build(start, end):
        if start >= end:
            return None

        nonlocal ind
        root_val = preorder[ind]
        mid = inorder_pos[root_val]
        root = TreeNode(root_val)

        root.left = build(start, mid)
        root.right = build(mid + 1, end)

        return root

    return build(0, len(preorder))


def build_from_in_post(inorder: List[int], postorder: List[int]) -> Optional[TreeNode]:
    inorder_pos = {val: ind for ind, val in enumerate(inorder)}
    ind = len(postorder) - 1
    pass


