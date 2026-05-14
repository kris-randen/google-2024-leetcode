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
            left: TreeNode = None,
            right: TreeNode = None
    ):
        self.val = val
        self.left = left
        self.right = right


def is_leaf(node: Optional[TreeNode]) -> bool:
    return \
    (
        node is not None and
        node.left is None and
        node.right is None
    )


def preorder_nodes(root: Optional[TreeNode]) -> Iterator[TreeNode]:
    if root is None:
        return

    yield root
    yield from preorder_nodes(root.left)
    yield from preorder_nodes(root.right)

def inorder_nodes(root: Optional[TreeNode]) -> Iterator[TreeNode]:
    if root is None:
        return

    yield from inorder_nodes(root.left)
    yield root
    yield from inorder_nodes(root.right)


def postorder_nodes(root: Optional[TreeNode]) -> Iterator[TreeNode]:
    if root is None:
        return

    yield from postorder_nodes(root.left)
    yield from postorder_nodes(root.right)
    yield root

Frame = tuple[Optional[TreeNode], bool]

def preorder_iter(root: Optional[TreeNode]) -> Iterator[TreeNode]:
    stack: List[Frame] = [(root, False)]

    while stack:
        node, emit = stack.pop()

        if node is None:
            continue

        if emit:
            yield node
        else:
            stack.append((node.right, False))
            stack.append((node.left, False))
            stack.append((node, True))

def inorder_iter(root: Optional[TreeNode]) -> Iterator[TreeNode]:
    stack: List[Frame] = [(root, False)]

    while stack:
        node, emit = stack.pop()

        if node is None:
            continue

        if emit:
            yield node
        else:
            stack.append((node.right, False))
            stack.append((node, True))
            stack.append((node.left, False))

def postorder_iter(root: Optional[TreeNode]) -> Iterator[TreeNode]:
    stack: List[Frame] = [(root, False)]

    while stack:
        node, emit = stack.pop()

        if node is None:
            continue

        if emit:
            yield node
        else:
            stack.append((node, True))
            stack.append((node.right, False))
            stack.append((node.left, False))

def level_order(root: Optional[TreeNode]) -> Iterator[List[TreeNode]]:
    if root is None:
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


def bfs_with_pos(root: Optional[TreeNode]) -> Iterator[tuple[int, int, int, Optional[TreeNode]]]:
    if root is None:
        return

    q = deque([(0, 0, root.val, root)])

    while q:
        col, row, val, node = q.popleft()
        yield col, row, val, node

        if left := node.left:
            q.append((col - 1, row + 1, left.val, left))
        if right := node.right:
            q.append((col + 1, row + 1, right.val, right))

def vertical_order(root: Optional[TreeNode]):
    cols = defaultdict(list)

    for col, row, val, node in bfs_with_pos(root):
        cols[col].append((col, row, val))

    return [cols[c] for c in sorted(cols)]


def build_from_pi(
        preorder: List[int],
        inorder: List[int]
) -> Optional[TreeNode]:
    inorder_ind = {val: ind for ind, val in enumerate(inorder)}
    root_ind = 0

    def build(start, end):
        if start >= end:
            return None

        nonlocal root_ind
        root_val = preorder[root_ind]
        root_ind += 1
        mid = inorder_ind[root_val]

        root = TreeNode(root_val)
        root.left = build(start, mid)
        root.right = build(mid + 1, end)

        return root

    return build(0, len(preorder))





def build_from_ip(inorder: List[int], postorder: List[int]):
    inorder_ind = {val: ind for ind, val in enumerate(inorder)}
    root_ind = len(postorder) - 1

    def build(start, end):
        if start >= end:
            return None

        nonlocal root_ind
        root_val = postorder[root_ind]
        root_ind -= 1

        mid = inorder_ind[root_val]

        root = TreeNode(root_val)
        root.right = build(mid + 1, end)
        root.left = build(start, mid)

        return root

    return build(0, len(postorder))


def build_from_pp(preorder: List[int], postorder: List[int]):
    post_pos_ind = {val: ind for ind, val in enumerate(postorder)}
    pre_l, pre_r = 0, (m := len(preorder)) - 1
    post_l, post_r = 0, (n := len(postorder)) - 1

    def left_size(pre_l, post_l):
        left_root = preorder[pre_l + 1]
        left_root_post_ind = post_pos_ind[left_root]
        return left_root_post_ind - post_l + 1

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

        size = left_size(pre_l, post_l)
        root.left = build(
            pre_l + 1,
            pre_l + 1 + size,
            post_l,
            post_l + size
        )

        root.right = build(
            pre_l + 1 + size,
            pre_r,
            post_l + size,
            post_r - 1
        )

        return root

    return build(0, m, 0, n)

NULL, SEP = "#", ","

def tree_to_tokens(root: Optional[TreeNode]) -> Iterator[str]:
    if root is None:
        yield NULL
        return

    yield str(root.val)
    yield from tree_to_tokens(root.left)
    yield from tree_to_tokens(root.right)

def tokens_to_tree(tokens: Iterator[str]) -> Optional[TreeNode]:
    token = next(tokens)

    if token == NULL:
        return None

    root = TreeNode(int(token))
    root.left = tokens_to_tree(tokens)
    root.right = tokens_to_tree(tokens)

    return root

def encode(tokens: Iterator[str]) -> str:
    return SEP.join(tokens)

def decode(data: str) -> Iterator[str]:
    return iter(data.split(SEP))

def serialize(root: Optional[TreeNode]) -> str:
    return encode(tree_to_tokens(root))

def deserialize(data: str) -> Optional[TreeNode]:
    return tokens_to_tree(decode(data))


"""

Linked List

"""

class ListNode:
    def __init__(self, val: int = 0, next: Optional[ListNode] = None):
        self.val = val
        self.next = next

    def __iter__(self):
        node = self

        while node:
            nxt = node.next
            yield node
            node = nxt

def nodes_iter(head: Optional[ListNode]) -> Iterator[ListNode]:
    return iter(()) if head is None else iter(head)


def values_iter(nodes: Iterator[ListNode]) -> Iterator[int]:
    return (node.val for node in nodes)


def detach_front(head: ListNode) -> tuple[ListNode, Optional[ListNode]]:
    rest = head.next
    head.next = None
    return head, rest

def attach_after(tail: ListNode, node: ListNode) -> Optional[ListNode]:
    tail.next = node
    return node

def cut_after(prev: ListNode) -> Optional[ListNode]:
    rest = prev.next
    prev.next = None
    return rest

def delete_after(prev: ListNode) -> Optional[ListNode]:
    target = prev.next

    if target is None:
        return None

    prev.next = target.next
    target.next = None
    return target

def reverse(head: Optional[ListNode]):
    prev, curr = None, head

    while curr:
        nxt = curr.next
        curr.next = prev
        prev = curr
        curr = nxt

    return prev

def reverse_prefix(head: Optional[ListNode], k):
    prev, curr, tail = None, head, head

    for _ in range(k):
        if curr is None:
            raise ValueError(f"List doesn't have k = {k} nodes.")

        nxt = curr.next
        curr.next = prev
        prev = curr
        curr = nxt

    return prev, tail, curr


def move_slow_fast(slow: ListNode, fast: ListNode):
    return slow.next, fast.next.next

def right_middle(head: Optional[ListNode]) -> Optional[ListNode]:
    slow = fast = head

    while fast and fast.next:
        slow, fast = move_slow_fast(slow, fast)

    return slow

def left_middle(head: Optional[ListNode]) -> Optional[ListNode]:
    if head is None or head.next is None:
        return head

    slow, fast = head, head.next

    while fast and fast.next:
        slow, fast = move_slow_fast(slow, fast)

    return slow

def split(head: Optional[ListNode]) -> tuple[Optional[ListNode], Optional[ListNode]]:
    if head is None or head.next is None:
        return head, None

    mid = left_middle(head)
    rest = cut_after(mid)

    return head, rest


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

def merge(a: Optional[ListNode], b: Optional[ListNode]):
    dummy = tail = ListNode()

    while a and b:
        if a.val <= b.val:
            node, a = detach_front(a)
        else:
            node, b = detach_front(b)
        tail = attach_after(tail, node)

    tail.next = a or b

    return dummy.next

def sort(head: Optional[ListNode]):
    if head is None or head.next is None:
        return head

    left, right = split(head)

    return merge(
        sort(left),
        sort(right)
    )

