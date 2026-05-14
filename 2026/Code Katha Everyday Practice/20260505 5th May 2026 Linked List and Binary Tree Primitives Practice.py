from __future__ import annotations

from typing import Optional, Iterator, List, Iterable


class TreeNode:
    def __init__(
            self,
            val: int=0,
            left: Optional[TreeNode]=None,
            right: Optional[TreeNode]=None
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


def tree_from_pi(preorder: List[int], inorder: List[int]):
    index = {val: ind for ind, val in enumerate(inorder)}
    ind = 0

    def rec(start, end):
        nonlocal ind

        if start >= end:
            return None

        val = preorder[ind]
        mid = index[val]
        ind += 1

        root = TreeNode(val)
        root.left = rec(start, mid)
        root.right = rec(mid + 1, end)

        return root

    return rec(0, len(preorder))


def tree_from_ip(inorder: List[int], postorder: List[int]):
    index = {val: ind for ind, val in enumerate(inorder)}
    ind = (n := len(postorder)) - 1

    def rec(start, end):
        nonlocal ind

        if start >= end:
            return None

        val = postorder[ind]
        mid = index[val]
        ind -= 1

        root = TreeNode(val)
        root.right = rec(mid + 1, end)
        root.left = rec(start, mid)

        return root

    return rec(0, n)

def tree_from_pp(preorder: List[int], postorder: List[int]):
    post_pos = {val: ind for ind, val in enumerate(postorder)}

    def size_left(pre_l, post_l):
        root = preorder[pre_l]
        root_post_pos_i = post_pos[root]
        return root_post_pos_i - post_l + 1

    def build(
            pre_l,
            pre_r,
            post_l,
            post_r
    ):
        if pre_l >= pre_r:
            return None

        root = TreeNode(preorder[pre_l])

        if pre_r - pre_l == 1:
            return root

        size = size_left(pre_l, post_l)

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
    return build(0, len(preorder), 0, len(postorder))

NULL, SEP = "#", ","

def tree_to_tokens_preorder(root: Optional[TreeNode]) -> Iterator[str]:
    if root is None:
        yield NULL
        return

    yield str(root.val)
    yield from tree_to_tokens_preorder(root.left)
    yield from tree_to_tokens_preorder(root.right)

def tree_from_tokens_preorder(tokens: Iterator[str]) -> Optional[TreeNode]:
    token = next(tokens)

    if token == NULL:
        return None

    root = TreeNode(int(token))
    root.left = tree_from_tokens_preorder(tokens)
    root.right = tree_from_tokens_preorder(tokens)

    return root

def encode(tokens: Iterator[str]) -> str:
    return SEP.join(tokens)

def decode(data: str) -> Iterator[str]:
    return iter(data.split(SEP))

def serialize(root: Optional[TreeNode]) -> str:
    return encode(tree_to_tokens_preorder(root))

def deserialize(data: str) -> Optional[TreeNode]:
    return tree_from_tokens_preorder(decode(data))
















"""

Linked List Primitives

"""

class Node:
    def __init__(
            self,
            val: int=0,
            nxt: Optional[Node]=None
    ):
        self.val = val
        self.next = nxt

    def __iter__(self):
        node = self

        while node:
            nxt = node.next
            yield node
            node = nxt


def nodes(head: Optional[Node]) -> Iterator[Node]:
    return iter(head) if head is not None else iter(())


def detach_head(head: Optional[Node]) -> tuple[Optional[Node], Optional[Node]]:
    rest = head.next
    head.next = None
    return head, rest

def attach_after(tail: Optional[Node], node: Optional[Node]):
    tail.next = node
    return node

def delete_after(prev: Optional[Node]):
    target = prev.next
    prev.next = target.next
    target.next = None
    return target

def cut_after(prev: Optional[Node]):
    rest = prev.next
    prev.next = None
    return rest

def move_slow_fast(slow: Optional[Node], fast: Optional[Node]):
    return slow.next, fast.next.next

def right_middle(head: Optional[Node]) -> Optional[Node]:
    slow = fast = head

    while fast and fast.next:
        slow, fast = move_slow_fast(slow, fast)

    return slow

def left_middle(head: Optional[Node]) -> Optional[Node]:
    slow, fast = head, head.next

    while fast and fast.next:
        slow, fast = move_slow_fast(slow, fast)

    return slow

def split(head: Optional[Node]) -> tuple[Optional[Node], Optional[Node]]:
    if head is None or head.next is None:
        return head, None

    mid = left_middle(head)
    rest = cut_after(mid)

    return head, rest



def reverse(head: Optional[Node]) -> Optional[Node]:
    prev, curr = None, head

    while curr:
        nxt = curr.next
        curr.next = prev
        prev = curr
        curr = next

    return prev

def reverse_prefix(head: Optional[Node], k):
    prev, curr = None, head

    for _ in range(k):
        if curr is None:
            raise ValueError(f"List doesn't have k = {k} nodes.")

        nxt = curr.next
        curr.next = prev
        prev = curr
        curr = nxt

    return prev, head, curr

def merge_sorted(a: Optional[Node], b: Optional[Node]):
    dummy = tail = Node(0)

    while a and b:
        if a.val <= b.val:
            node, a = detach_head(a)
        else:
            node, b = detach_head(b)
        tail = attach_after(tail, node)

    tail.next = a or b
    return dummy.next

def weave(a: Optional[Node], b: Optional[Node]):
    dummy = tail = Node(0)

    while a or b:
        if a:
            node, a = detach_head(a)
            tail = attach_after(tail, node)
        if b:
            node, b = detach_head(b)
            tail = attach_after(tail, node)

    return dummy.next



