"""

Code Katha

"""


from __future__ import annotations
from collections import deque, defaultdict
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


def reverse_prefix(x: Optional[ListNode], k: int) -> tuple[Optional[ListNode], Optional[ListNode], Optional[ListNode]]:
    if not x or k <= 0:
        return None, None, x

    prev, tail, curr = None, x, x
    for _ in range(k):
        if not curr: break
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
        update(self)

    def open(self):
        return self.val, self.left, self.right


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

        val = preorder[pre_l]
        root = TreeNode(val)
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

    val, left, right = root.open()

    if key < val:
        return get(left, key)
    elif key == val:
        return root
    else:
        return get(right, key)


def contains(root: Optional[TreeNode], key: int) -> bool:
    return get(root, key) is not None


def put(root: Optional[TreeNode], key: int) -> Optional[TreeNode]:
    if not root:
        return TreeNode(key)

    val, left, right = root.open()

    if key < val:
        root.left = put(left, key)
    elif key == val:
        root.val = key
    else:
        root.right = put(right, key)

    return update(root)


def delete_min(root: Optional[TreeNode]) -> Optional[TreeNode]:
    if not root:
        return None

    val, left, right = root.open()

    if not left:
        return right

    root.left = delete_min(left)
    return update(root)


def delete_max(root: Optional[TreeNode]) -> Optional[TreeNode]:
    if not root:
        return None

    val, left, right = root.open()

    if not right:
        return left

    root.right = delete_max(right)
    return update(root)


def delete(root: Optional[TreeNode], key: int) -> Optional[TreeNode]:
    if not root:
        return None

    val, left, right = root.open()

    if key < val:
        root.left = delete(left, key)
    elif key > val:
        root.right = delete(right, key)
    else:
        if not left:
            return right
        if not right:
            return left

        successor = leftmost(right)
        successor.right = delete_min(right)
        successor.left = left
        root = successor

    return update(root)


def floor(root: Optional[TreeNode], key: int) -> Optional[TreeNode]:
    if not root:
        return None

    val, left, right = root.open()

    if key < val:
        return floor(left, key)
    elif key == val:
        return root
    else:
        return floor(right, key) or root


def ceil(root: Optional[TreeNode], key: int) -> Optional[TreeNode]:
    if not root:
        return None

    val, left, right = root.open()

    if key > val:
        return ceil(right, key)
    elif key == val:
        return root
    else:
        return ceil(left, key) or root


def pred(root: Optional[TreeNode], key: int) -> Optional[TreeNode]:
    if not root:
        return None

    val, left, right = root.open()

    if key <= val:
        return pred(left, key)
    else:
        return pred(right, key) or root


def succ(root: Optional[TreeNode], key: int) -> Optional[TreeNode]:
    if not root:
        return None

    val, left, right = root.open()

    if key >= val:
        return succ(right, key)
    else:
        return succ(left, key) or root


def predecessor(p: Optional[TreeNode]) -> Optional[TreeNode]:
    if not p:
        return None

    if p.left:
        return rightmost(p.left)

    while is_left_child(p):
        p = p.parent

    return p.parent


def successor(p: Optional[TreeNode]) -> Optional[TreeNode]:
    if not p:
        return None

    if p.right:
        return leftmost(p.right)

    while is_right_child(p):
        p = p.parent

    return p.parent


def rank(root: Optional[TreeNode], key: int) -> int:
    if not root:
        return 0

    val, left, right = root.open()

    if key < val:
        return rank(left, key)
    elif key == val:
        return size(left)
    else:
        return 1 + size(left) + rank(right, key)


def select(root: Optional[TreeNode], order: int) -> Optional[TreeNode]:
    if not root:
        return None

    val, left, right = root.open()

    if order < size(left):
        return select(left, order)
    elif order == size(left):
        return root
    else:
        return select(right, order - 1 - size(left))


def range_count(root: Optional[TreeNode], lo: int, hi: int) -> int:
    if lo > hi: return 0
    return rank(root, hi) - rank(root, lo) + int(contains(root, hi))


def range_nodes(root: Optional[TreeNode], lo: int, hi: int) -> Iterator[TreeNode]:
    if not root: return

    val, left, right = root.open()

    if lo < val:
        yield from range_nodes(left, lo, hi)
    if lo <= val <= hi:
        yield root
    if val < hi:
        yield from range_nodes(right, lo, hi)


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

        return None, hasp, has_q

    lca, has_p, has_q = dfs(root)
    return lca if has_p and has_q else None


def lca_bst(root: Optional[TreeNode], a: int, b: int) -> Optional[TreeNode]:
    if not root:
        return None

    lo, hi = min(a, b), max(a, b)
    val, left, right = root.open()

    if lo > val:
        return lca_bst(right, lo, hi)
    elif hi < val:
        return lca_bst(left, lo, hi)
    else:
        return root


def lca_bst_non_guaranteed(root: Optional[TreeNode], a: int, b: int) -> Optional[TreeNode]:
    if not contains(root, a) or not contains(root, b): return None
    return lca_bst(root, a, b)