"""
BST Katha — Clean Skeletal Toolkit
==================================

This file is organized around solution skeletons, not around LeetCode IDs
scattered through every primitive.

The structure is:

    0. Representation / test helpers
    1. Low-level BST primitives
    2. Skeleton A — Ordered descent
    3. Skeleton B — Candidate-tracking ordered descent
    4. Skeleton C — First split point
    5. Skeleton D — Inorder sorted stream
    6. Skeleton E — Bounds recursion
    7. Skeleton F — Local rewiring
    8. Skeleton G — Reverse inorder accumulation
    9. Skeleton H — Sorted data -> balanced BST
    10. Skeleton I — Preorder + bounds
    11. Skeleton J — Root-split recurrence
    12. Skeleton K — Multi-BST stream/set logic
    13. Skeleton L — Postorder BST certificate
    14. Skeleton M — Ordered-symbol-table augmentation
    15. Skeleton N — LLRB balanced tree awareness
    16. Problem map and drill order

Core BST superpowers:

    1. Ordered descent:
        Values tell us whether to go left or right.

    2. Sorted projection:
        Inorder traversal turns a BST into a sorted stream.

Most BST problems reduce to one of these skeletons:

    A. Ordered descent
    B. Candidate-tracking ordered descent
    C. First split point
    D. Inorder sorted stream
    E. Bounds recursion
    F. Local rewiring
    G. Reverse inorder accumulation
    H. Sorted data -> balanced BST
    I. Preorder + bounds
    J. Root-split recurrence
    K. Multi-BST stream/set logic
    L. Postorder BST certificate
    M. Augmented ordered tree
    N. LLRB balanced tree
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from enum import Enum
from math import comb
from typing import Iterable, Iterator, Optional


# =============================================================================
# 0. Representation / test helpers
# =============================================================================

class TreeNode:
    def __init__(
        self,
        val: int = 0,
        left: Optional["TreeNode"] = None,
        right: Optional["TreeNode"] = None,
    ):
        self.val = val
        self.left = left
        self.right = right


class ListNode:
    def __init__(self, val: int = 0, next: Optional["ListNode"] = None):
        self.val = val
        self.next = next


def clone(root: Optional[TreeNode]) -> Optional[TreeNode]:
    if root is None:
        return None
    return TreeNode(root.val, clone(root.left), clone(root.right))


def same_tree(a: Optional[TreeNode], b: Optional[TreeNode]) -> bool:
    if a is None or b is None:
        return a is b

    return (
        a.val == b.val
        and same_tree(a.left, b.left)
        and same_tree(a.right, b.right)
    )


def size(root: Optional[TreeNode]) -> int:
    if root is None:
        return 0
    return 1 + size(root.left) + size(root.right)


def height(root: Optional[TreeNode]) -> int:
    if root is None:
        return 0
    return 1 + max(height(root.left), height(root.right))


def insert(root: Optional[TreeNode], val: int) -> TreeNode:
    """
    Plain unbalanced BST insert.

    Skeleton:
        ordered descent + attach at null slot.
    """
    if root is None:
        return TreeNode(val)

    if val < root.val:
        root.left = insert(root.left, val)
    elif val > root.val:
        root.right = insert(root.right, val)

    return root


def bst_from(values: Iterable[int]) -> Optional[TreeNode]:
    root = None
    for val in values:
        root = insert(root, val)
    return root


# =============================================================================
# 1. Low-level BST primitives
# =============================================================================

def leftmost(root: TreeNode) -> TreeNode:
    """
    Smallest node in a BST subtree.
    """
    while root.left:
        root = root.left
    return root


def rightmost(root: TreeNode) -> TreeNode:
    """
    Largest node in a BST subtree.
    """
    while root.right:
        root = root.right
    return root


def min_val(root: TreeNode) -> int:
    return leftmost(root).val


def max_val(root: TreeNode) -> int:
    return rightmost(root).val


# =============================================================================
# 2. Skeleton A — Ordered descent
# =============================================================================

def search(root: Optional[TreeNode], val: int) -> Optional[TreeNode]:
    """
    Exact lookup by ordered descent.

    Each comparison discards one whole subtree.
    """
    while root:
        if val < root.val:
            root = root.left
        elif val > root.val:
            root = root.right
        else:
            return root
    return None


def contains(root: Optional[TreeNode], val: int) -> bool:
    return search(root, val) is not None


# =============================================================================
# 3. Skeleton B — Candidate-tracking ordered descent
# =============================================================================

def floor(root: Optional[TreeNode], val: int) -> Optional[TreeNode]:
    """
    Largest node with value <= val.
    """
    ans = None

    while root:
        if root.val <= val:
            ans = root
            root = root.right
        else:
            root = root.left

    return ans


def ceiling(root: Optional[TreeNode], val: int) -> Optional[TreeNode]:
    """
    Smallest node with value >= val.
    """
    ans = None

    while root:
        if root.val >= val:
            ans = root
            root = root.left
        else:
            root = root.right

    return ans


def predecessor(root: Optional[TreeNode], val: int) -> Optional[TreeNode]:
    """
    Largest node with value < val.
    """
    ans = None

    while root:
        if root.val < val:
            ans = root
            root = root.right
        else:
            root = root.left

    return ans


def successor(root: Optional[TreeNode], val: int) -> Optional[TreeNode]:
    """
    Smallest node with value > val.
    """
    ans = None

    while root:
        if root.val > val:
            ans = root
            root = root.left
        else:
            root = root.right

    return ans


def closest_value(root: Optional[TreeNode], target: float) -> int:
    """
    Candidate-tracking descent with absolute-distance comparison.
    """
    if root is None:
        raise ValueError("closest_value requires a non-empty BST")

    best = root.val

    while root:
        if abs(root.val - target) < abs(best - target):
            best = root.val

        root = root.left if target < root.val else root.right

    return best


# =============================================================================
# 4. Skeleton C — First split point
# =============================================================================

def lca(root: Optional[TreeNode], p: TreeNode, q: TreeNode) -> Optional[TreeNode]:
    """
    Lowest common ancestor in a BST.

    The answer is the first node where p and q stop going to the same side.
    """
    lo = min(p.val, q.val)
    hi = max(p.val, q.val)

    while root:
        if hi < root.val:
            root = root.left
        elif lo > root.val:
            root = root.right
        else:
            return root

    return None


# =============================================================================
# 5. Skeleton D — Inorder sorted stream
# =============================================================================

def preorder(root: Optional[TreeNode]) -> Iterator[TreeNode]:
    if root is None:
        return

    yield root
    yield from preorder(root.left)
    yield from preorder(root.right)


def inorder(root: Optional[TreeNode]) -> Iterator[TreeNode]:
    """
    The central BST stream.

    For a valid BST:
        inorder(root) emits nodes in sorted order.
    """
    if root is None:
        return

    yield from inorder(root.left)
    yield root
    yield from inorder(root.right)


def reverse_inorder(root: Optional[TreeNode]) -> Iterator[TreeNode]:
    """
    Descending sorted stream.
    """
    if root is None:
        return

    yield from reverse_inorder(root.right)
    yield root
    yield from reverse_inorder(root.left)


def preorder_vals(root: Optional[TreeNode]) -> Iterator[int]:
    return (node.val for node in preorder(root))


def inorder_vals(root: Optional[TreeNode]) -> Iterator[int]:
    return (node.val for node in inorder(root))


def preorder_list(root: Optional[TreeNode]) -> list[int]:
    return list(preorder_vals(root))


def inorder_list(root: Optional[TreeNode]) -> list[int]:
    return list(inorder_vals(root))


def is_valid_bst_by_inorder(root: Optional[TreeNode]) -> bool:
    prev = None

    for val in inorder_vals(root):
        if prev is not None and val <= prev:
            return False
        prev = val

    return True


def kth_smallest(root: Optional[TreeNode], k: int) -> int:
    for i, node in enumerate(inorder(root), start=1):
        if i == k:
            return node.val

    raise ValueError("tree has fewer than k nodes")


def min_abs_diff(root: Optional[TreeNode]) -> int:
    prev = None
    best = float("inf")

    for val in inorder_vals(root):
        if prev is not None:
            best = min(best, val - prev)
        prev = val

    return int(best)


def modes(root: Optional[TreeNode]) -> list[int]:
    """
    Run-length counting over the inorder stream.
    """
    prev = None
    run = 0
    best = 0
    ans = []

    for val in inorder_vals(root):
        if val == prev:
            run += 1
        else:
            prev = val
            run = 1

        if run > best:
            best = run
            ans = [val]
        elif run == best:
            ans.append(val)

    return ans


def recover_bst(root: Optional[TreeNode]) -> None:
    """
    Recover two swapped nodes by detecting inorder inversions.
    """
    first = second = prev = None

    for curr in inorder(root):
        if prev is not None and curr.val < prev.val:
            if first is None:
                first = prev
            second = curr
        prev = curr

    if first and second:
        first.val, second.val = second.val, first.val


class BSTIterator:
    """
    Lazy inorder iterator.

    Stack invariant:
        stack stores the path to the next smallest unconsumed node.
    """

    def __init__(self, root: Optional[TreeNode]):
        self.stack: list[TreeNode] = []
        self.push_left(root)

    def push_left(self, root: Optional[TreeNode]) -> None:
        while root:
            self.stack.append(root)
            root = root.left

    def next(self) -> int:
        node = self.stack.pop()
        self.push_left(node.right)
        return node.val

    def hasNext(self) -> bool:
        return bool(self.stack)


class BSTIteratorII:
    """
    Bidirectional iterator.

    Composition:
        lazy forward inorder stream
        history array
        index into history
    """

    def __init__(self, root: Optional[TreeNode]):
        self.forward = BSTIterator(root)
        self.history: list[int] = []
        self.i = -1

    def hasNext(self) -> bool:
        return self.i + 1 < len(self.history) or self.forward.hasNext()

    def next(self) -> int:
        if self.i + 1 == len(self.history):
            self.history.append(self.forward.next())

        self.i += 1
        return self.history[self.i]

    def hasPrev(self) -> bool:
        return self.i > 0

    def prev(self) -> int:
        self.i -= 1
        return self.history[self.i]


# =============================================================================
# 6. Skeleton E — Bounds recursion
# =============================================================================

def is_valid_bst(root: Optional[TreeNode]) -> bool:
    """
    Recursive open-interval validation:
        low < node.val < high
    """

    def valid(node: Optional[TreeNode], low: Optional[int], high: Optional[int]) -> bool:
        if node is None:
            return True

        if low is not None and node.val <= low:
            return False

        if high is not None and node.val >= high:
            return False

        return valid(node.left, low, node.val) and valid(node.right, node.val, high)

    return valid(root, None, None)


# =============================================================================
# 7. Skeleton F — Local rewiring
# =============================================================================

def range_sum(root: Optional[TreeNode], low: int, high: int) -> int:
    """
    Range pruning without modifying the tree.
    """
    if root is None:
        return 0

    if root.val < low:
        return range_sum(root.right, low, high)

    if root.val > high:
        return range_sum(root.left, low, high)

    return root.val + range_sum(root.left, low, high) + range_sum(root.right, low, high)


def trim(root: Optional[TreeNode], low: int, high: int) -> Optional[TreeNode]:
    """
    Range pruning with subtree reconnecting.
    """
    if root is None:
        return None

    if root.val < low:
        return trim(root.right, low, high)

    if root.val > high:
        return trim(root.left, low, high)

    root.left = trim(root.left, low, high)
    root.right = trim(root.right, low, high)
    return root


def split(root: Optional[TreeNode], target: int) -> tuple[Optional[TreeNode], Optional[TreeNode]]:
    """
    Return:
        first tree  -> values <= target
        second tree -> values > target
    """
    if root is None:
        return None, None

    if root.val <= target:
        small_from_right, right = split(root.right, target)
        root.right = small_from_right
        return root, right

    left, large_from_left = split(root.left, target)
    root.left = large_from_left
    return left, root


def delete_min(root: TreeNode) -> Optional[TreeNode]:
    """
    Delete the smallest node from a subtree.
    """
    if root.left is None:
        return root.right

    root.left = delete_min(root.left)
    return root


def delete(root: Optional[TreeNode], val: int) -> Optional[TreeNode]:
    """
    Hibbard deletion.

    This function returns the new root of the modified subtree.
    """
    if root is None:
        return None

    if val < root.val:
        root.left = delete(root.left, val)
        return root

    if val > root.val:
        root.right = delete(root.right, val)
        return root

    if root.left is None:
        return root.right

    if root.right is None:
        return root.left

    nxt = leftmost(root.right)
    nxt.right = delete_min(root.right)
    nxt.left = root.left
    return nxt


def increasing_tree(root: Optional[TreeNode]) -> Optional[TreeNode]:
    """
    Inorder rewiring into a right-only increasing chain.
    """
    dummy = tail = TreeNode()

    for node in inorder(root):
        node.left = None
        tail.right = node
        tail = node

    tail.right = None
    return dummy.right


def bst_to_doubly_list(root: Optional[TreeNode]) -> Optional[TreeNode]:
    """
    Inorder rewiring into a circular doubly linked list.

    Uses:
        left  as prev
        right as next
    """
    if root is None:
        return None

    first = last = None

    for curr in inorder(root):
        curr.left = last

        if last:
            last.right = curr
        else:
            first = curr

        last = curr

    first.left = last
    last.right = first

    return first


# =============================================================================
# 8. Skeleton G — Reverse inorder accumulation
# =============================================================================

def greater_sum_tree(root: Optional[TreeNode]) -> Optional[TreeNode]:
    """
    Descending stream + running total.
    """
    total = 0

    for node in reverse_inorder(root):
        total += node.val
        node.val = total

    return root


# =============================================================================
# 9. Skeleton H — Sorted data -> balanced BST
# =============================================================================

def sorted_array_to_bst(nums: list[int]) -> Optional[TreeNode]:
    """
    Median-root construction from sorted array.
    """

    def build(lo: int, hi: int) -> Optional[TreeNode]:
        if lo >= hi:
            return None

        mid = (lo + hi) // 2
        return TreeNode(
            nums[mid],
            build(lo, mid),
            build(mid + 1, hi),
        )

    return build(0, len(nums))


def sorted_list_to_bst(head: Optional[ListNode]) -> Optional[TreeNode]:
    """
    Build a balanced BST by consuming the sorted list in inorder.
    """
    n = 0
    curr = head

    while curr:
        n += 1
        curr = curr.next

    curr = head

    def build(count: int) -> Optional[TreeNode]:
        nonlocal curr

        if count == 0:
            return None

        left = build(count // 2)

        root = TreeNode(curr.val)
        root.left = left
        curr = curr.next

        root.right = build(count - count // 2 - 1)
        return root

    return build(n)


def balance_bst(root: Optional[TreeNode]) -> Optional[TreeNode]:
    """
    Existing BST -> sorted array -> balanced BST.
    """
    return sorted_array_to_bst(inorder_list(root))


# =============================================================================
# 10. Skeleton I — Preorder + bounds
# =============================================================================

def bst_from_preorder(pre: list[int]) -> Optional[TreeNode]:
    """
    Build a BST from preorder using an upper bound.
    """
    i = 0

    def build(upper: float) -> Optional[TreeNode]:
        nonlocal i

        if i == len(pre) or pre[i] > upper:
            return None

        val = pre[i]
        i += 1

        root = TreeNode(val)
        root.left = build(val)
        root.right = build(upper)
        return root

    return build(float("inf"))


def verify_preorder(pre: list[int]) -> bool:
    """
    Verify a BST preorder sequence using a monotonic stack.

    lower is the last ancestor whose right subtree we entered.
    """
    stack = []
    lower = float("-inf")

    for val in pre:
        if val <= lower:
            return False

        while stack and val > stack[-1]:
            lower = stack.pop()

        stack.append(val)

    return True


SEP = ","

def serialize(root: Optional[TreeNode]) -> str:
    """
    Compact BST serialization.

    Preorder alone is enough because BST bounds disambiguate reconstruction.
    """
    return SEP.join(str(x) for x in preorder_vals(root))


def deserialize(data: str) -> Optional[TreeNode]:
    if not data:
        return None

    return bst_from_preorder([int(x) for x in data.split(SEP)])


# =============================================================================
# 11. Skeleton J — Root-split recurrence
# =============================================================================

def generate_trees(n: int) -> list[Optional[TreeNode]]:
    """
    Generate all structurally unique BSTs storing values 1..n.
    """

    def build(lo: int, hi: int) -> list[Optional[TreeNode]]:
        if lo > hi:
            return [None]

        ans = []

        for root_val in range(lo, hi + 1):
            for left in build(lo, root_val - 1):
                for right in build(root_val + 1, hi):
                    ans.append(TreeNode(root_val, left, right))

        return ans

    return build(1, n)


def count_unique_bsts(n: int) -> int:
    """
    Catalan DP via root-split recurrence.
    """
    dp = [0] * (n + 1)
    dp[0] = 1

    for count in range(1, n + 1):
        for left_count in range(count):
            right_count = count - 1 - left_count
            dp[count] += dp[left_count] * dp[right_count]

    return dp[n]


MOD = 10**9 + 7

def reorderings_same_bst(nums: list[int]) -> int:
    """
    Count reorderings that produce the same BST.

    Root is fixed as nums[0].
    Left and right subsequences must preserve their internal relative order.
    """
    def ways(arr: list[int]) -> int:
        if len(arr) <= 2:
            return 1

        root = arr[0]
        left = [x for x in arr[1:] if x < root]
        right = [x for x in arr[1:] if x > root]

        return (
            comb(len(left) + len(right), len(left))
            * ways(left)
            * ways(right)
        ) % MOD

    return (ways(nums) - 1) % MOD


# =============================================================================
# 12. Skeleton K — Multi-BST stream/set logic
# =============================================================================

def two_sum_bst(root: Optional[TreeNode], target: int) -> bool:
    seen = set()

    for val in inorder_vals(root):
        if target - val in seen:
            return True
        seen.add(val)

    return False


def two_sum_bsts(a: Optional[TreeNode], b: Optional[TreeNode], target: int) -> bool:
    vals = set(inorder_vals(a))
    return any(target - x in vals for x in inorder_vals(b))


def merge_sorted(a: Iterator[int], b: Iterator[int]) -> Iterator[int]:
    sentinel = object()
    x = next(a, sentinel)
    y = next(b, sentinel)

    while x is not sentinel and y is not sentinel:
        if x <= y:
            yield x
            x = next(a, sentinel)
        else:
            yield y
            y = next(b, sentinel)

    while x is not sentinel:
        yield x
        x = next(a, sentinel)

    while y is not sentinel:
        yield y
        y = next(b, sentinel)


def all_elements(a: Optional[TreeNode], b: Optional[TreeNode]) -> list[int]:
    return list(merge_sorted(inorder_vals(a), inorder_vals(b)))


def closest_nodes(root: Optional[TreeNode], queries: list[int]) -> list[list[int]]:
    import bisect

    vals = inorder_list(root)
    ans = []

    for q in queries:
        i = bisect.bisect_left(vals, q)

        lo = vals[i - 1] if i > 0 else -1
        hi = vals[i] if i < len(vals) else -1

        if i < len(vals) and vals[i] == q:
            lo = hi = q

        ans.append([lo, hi])

    return ans


# =============================================================================
# 13. Skeleton L — Postorder BST certificate
# =============================================================================

@dataclass
class Cert:
    is_bst: bool
    size: int
    min_val: int
    max_val: int
    sum_val: int


EMPTY_CERT = Cert(
    is_bst=True,
    size=0,
    min_val=float("inf"),
    max_val=float("-inf"),
    sum_val=0,
)

BAD_CERT = Cert(
    is_bst=False,
    size=0,
    min_val=float("-inf"),
    max_val=float("inf"),
    sum_val=0,
)


def largest_bst_subtree(root: Optional[TreeNode]) -> int:
    best = 0

    def dfs(node: Optional[TreeNode]) -> Cert:
        nonlocal best

        if node is None:
            return EMPTY_CERT

        left = dfs(node.left)
        right = dfs(node.right)

        if left.is_bst and right.is_bst and left.max_val < node.val < right.min_val:
            curr = Cert(
                is_bst=True,
                size=left.size + right.size + 1,
                min_val=min(left.min_val, node.val),
                max_val=max(right.max_val, node.val),
                sum_val=left.sum_val + right.sum_val + node.val,
            )
            best = max(best, curr.size)
            return curr

        return BAD_CERT

    dfs(root)
    return best


def max_sum_bst(root: Optional[TreeNode]) -> int:
    best = 0

    def dfs(node: Optional[TreeNode]) -> Cert:
        nonlocal best

        if node is None:
            return EMPTY_CERT

        left = dfs(node.left)
        right = dfs(node.right)

        if left.is_bst and right.is_bst and left.max_val < node.val < right.min_val:
            total = left.sum_val + right.sum_val + node.val
            best = max(best, total)

            return Cert(
                is_bst=True,
                size=left.size + right.size + 1,
                min_val=min(left.min_val, node.val),
                max_val=max(right.max_val, node.val),
                sum_val=total,
            )

        return BAD_CERT

    dfs(root)
    return best


def can_merge(trees: list[TreeNode]) -> Optional[TreeNode]:
    """
    Merge a forest of small BSTs by grafting matching leaf values.
    """
    roots = {t.val: t for t in trees}
    leaves = Counter()

    for t in trees:
        if t.left:
            leaves[t.left.val] += 1
        if t.right:
            leaves[t.right.val] += 1

    candidates = [t for t in trees if leaves[t.val] == 0]

    if len(candidates) != 1:
        return None

    root = candidates[0]
    used = set()

    def graft(node: Optional[TreeNode], low: int, high: int) -> bool:
        if node is None:
            return True

        if not (low < node.val < high):
            return False

        if node.left is None and node.right is None and node.val in roots and node is not roots[node.val]:
            other = roots[node.val]
            node.left = other.left
            node.right = other.right
            used.add(node.val)

        return graft(node.left, low, node.val) and graft(node.right, node.val, high)

    used.add(root.val)

    if not graft(root, float("-inf"), float("inf")):
        return None

    return root if len(used) == len(trees) else None


# =============================================================================
# 14. Skeleton M — Ordered-symbol-table augmentation
# =============================================================================

class SizedNode:
    """
    BST node augmented with subtree size.

    This supports:
        rank(key)  -> number of keys less than key
        select(k)  -> key with zero-based rank k
    """

    def __init__(
        self,
        key: int,
        left: Optional["SizedNode"] = None,
        right: Optional["SizedNode"] = None,
        count: int = 1,
    ):
        self.key = key
        self.left = left
        self.right = right
        self.count = count


def sized_count(root: Optional[SizedNode]) -> int:
    return root.count if root else 0


def fix_count(root: SizedNode) -> SizedNode:
    root.count = 1 + sized_count(root.left) + sized_count(root.right)
    return root


def sized_insert(root: Optional[SizedNode], key: int) -> SizedNode:
    if root is None:
        return SizedNode(key)

    if key < root.key:
        root.left = sized_insert(root.left, key)
    elif key > root.key:
        root.right = sized_insert(root.right, key)

    return fix_count(root)


def rank(root: Optional[SizedNode], key: int) -> int:
    """
    Number of keys < key.
    """
    if root is None:
        return 0

    if key < root.key:
        return rank(root.left, key)

    if key > root.key:
        return 1 + sized_count(root.left) + rank(root.right, key)

    return sized_count(root.left)


def select(root: Optional[SizedNode], k: int) -> Optional[SizedNode]:
    """
    Node with zero-based rank k.
    """
    if root is None:
        return None

    left_count = sized_count(root.left)

    if k < left_count:
        return select(root.left, k)

    if k > left_count:
        return select(root.right, k - left_count - 1)

    return root


def keys_between(root: Optional[SizedNode], lo: int, hi: int) -> Iterator[int]:
    if root is None:
        return

    if lo < root.key:
        yield from keys_between(root.left, lo, hi)

    if lo <= root.key <= hi:
        yield root.key

    if root.key < hi:
        yield from keys_between(root.right, lo, hi)


# =============================================================================
# 15. Skeleton N — LLRB balanced tree awareness
# =============================================================================

class Color(Enum):
    RED = True
    BLACK = False


class RBNode:
    """
    Left-leaning red-black tree node.

    The color belongs to the parent link.
    A red left link glues two BST nodes into one 3-node.
    Null links are black.
    """

    def __init__(
        self,
        key: int,
        color: Color = Color.RED,
        left: Optional["RBNode"] = None,
        right: Optional["RBNode"] = None,
        count: int = 1,
    ):
        self.key = key
        self.color = color
        self.left = left
        self.right = right
        self.count = count


def is_red(root: Optional[RBNode]) -> bool:
    return root is not None and root.color is Color.RED


def rb_count(root: Optional[RBNode]) -> int:
    return root.count if root else 0


def fix_rb_count(root: RBNode) -> RBNode:
    root.count = 1 + rb_count(root.left) + rb_count(root.right)
    return root


def rotate_left(h: RBNode) -> RBNode:
    """
    Fix a right-leaning red link.
    """
    x = h.right
    h.right = x.left
    x.left = h

    x.color = h.color
    h.color = Color.RED

    x.count = h.count
    fix_rb_count(h)
    return x


def rotate_right(h: RBNode) -> RBNode:
    """
    Fix two left red links in a row.
    """
    x = h.left
    h.left = x.right
    x.right = h

    x.color = h.color
    h.color = Color.RED

    x.count = h.count
    fix_rb_count(h)
    return x


def flip_colors(h: RBNode) -> None:
    """
    Split a temporary 4-node.
    """
    h.color = Color.RED if h.color is Color.BLACK else Color.BLACK

    if h.left:
        h.left.color = Color.BLACK if h.left.color is Color.RED else Color.RED

    if h.right:
        h.right.color = Color.BLACK if h.right.color is Color.RED else Color.RED


def balance_llrb(h: RBNode) -> RBNode:
    """
    Compact LLRB insertion repair:

        1. right red and not left red -> rotate left
        2. left red and left-left red -> rotate right
        3. both children red         -> flip colors
    """
    if is_red(h.right) and not is_red(h.left):
        h = rotate_left(h)

    if is_red(h.left) and is_red(h.left.left):
        h = rotate_right(h)

    if is_red(h.left) and is_red(h.right):
        flip_colors(h)

    return fix_rb_count(h)


def llrb_insert(root: Optional[RBNode], key: int) -> RBNode:
    def rec(h: Optional[RBNode]) -> RBNode:
        if h is None:
            return RBNode(key, Color.RED)

        if key < h.key:
            h.left = rec(h.left)
        elif key > h.key:
            h.right = rec(h.right)

        return balance_llrb(h)

    root = rec(root)
    root.color = Color.BLACK
    return root


# =============================================================================
# 16. Problem map and drill order
# =============================================================================

PROBLEM_MAP = {
    "ordered_descent": {
        "skeleton": "Search path discards one subtree per comparison.",
        "problems": [700, 701],
        "functions": ["search", "insert"],
    },
    "candidate_tracking_descent": {
        "skeleton": "Search path plus best-so-far candidate.",
        "problems": [270, 272, 285, 510, 2476],
        "functions": ["floor", "ceiling", "predecessor", "successor", "closest_value", "closest_nodes"],
    },
    "first_split_point": {
        "skeleton": "Walk while both targets are on same side; first split is answer.",
        "problems": [235],
        "functions": ["lca"],
    },
    "inorder_sorted_stream": {
        "skeleton": "BST -> inorder -> sorted stream.",
        "problems": [98, 99, 173, 230, 501, 530, 783, 1586],
        "functions": ["inorder", "is_valid_bst_by_inorder", "kth_smallest", "min_abs_diff", "modes", "recover_bst", "BSTIterator", "BSTIteratorII"],
    },
    "bounds_recursion": {
        "skeleton": "Carry open interval low < node.val < high downward.",
        "problems": [98, 1932],
        "functions": ["is_valid_bst", "can_merge"],
    },
    "local_rewiring": {
        "skeleton": "Modify subtree and return new subtree root.",
        "problems": [450, 669, 776, 897, 426],
        "functions": ["delete", "trim", "split", "increasing_tree", "bst_to_doubly_list"],
    },
    "reverse_inorder_accumulation": {
        "skeleton": "Descending stream plus running total.",
        "problems": [538, 1038],
        "functions": ["reverse_inorder", "greater_sum_tree"],
    },
    "balanced_construction": {
        "skeleton": "Sorted data -> median root -> balanced halves.",
        "problems": [108, 109, 1382],
        "functions": ["sorted_array_to_bst", "sorted_list_to_bst", "balance_bst"],
    },
    "preorder_bounds": {
        "skeleton": "Preorder gives root order; bounds decide subtree membership.",
        "problems": [255, 449, 1008],
        "functions": ["bst_from_preorder", "verify_preorder", "serialize", "deserialize"],
    },
    "root_split_recurrence": {
        "skeleton": "Choose/fix root, partition left/right, recursively combine.",
        "problems": [95, 96, 1569],
        "functions": ["generate_trees", "count_unique_bsts", "reorderings_same_bst"],
    },
    "multi_bst": {
        "skeleton": "Use sorted streams or hash sets across one/two BSTs.",
        "problems": [653, 1214, 1305],
        "functions": ["two_sum_bst", "two_sum_bsts", "merge_sorted", "all_elements"],
    },
    "postorder_certificate": {
        "skeleton": "Children return min/max/size/sum certificate; parent validates.",
        "problems": [333, 1373],
        "functions": ["Cert", "largest_bst_subtree", "max_sum_bst"],
    },
    "ordered_symbol_table": {
        "skeleton": "Augment each node with subtree size.",
        "problems": [703, 1902],
        "functions": ["rank", "select", "keys_between"],
    },
    "llrb_balanced_tree": {
        "skeleton": "2-3 tree represented by left-leaning red links.",
        "problems": ["conceptual interview awareness"],
        "functions": ["rotate_left", "rotate_right", "flip_colors", "balance_llrb", "llrb_insert"],
    },
}


DRILL_ORDER = [
    "leftmost / rightmost",
    "search / insert",
    "floor / ceiling / predecessor / successor",
    "closest_value",
    "lca as first split point",
    "inorder / reverse_inorder",
    "is_valid_bst / is_valid_bst_by_inorder",
    "kth_smallest / min_abs_diff / modes",
    "recover_bst",
    "BSTIterator / BSTIteratorII",
    "range_sum / trim",
    "delete_min / delete",
    "split",
    "greater_sum_tree",
    "increasing_tree / bst_to_doubly_list",
    "sorted_array_to_bst / sorted_list_to_bst / balance_bst",
    "bst_from_preorder / verify_preorder / serialize / deserialize",
    "generate_trees / count_unique_bsts / reorderings_same_bst",
    "two_sum_bst / two_sum_bsts / merge_sorted / all_elements",
    "Cert / largest_bst_subtree / max_sum_bst",
    "rank / select / keys_between",
    "LLRB rotate_left / rotate_right / flip_colors / llrb_insert",
]


# =============================================================================
# Smoke tests
# =============================================================================

def _test() -> None:
    root = bst_from([5, 3, 7, 2, 4, 6, 8])

    assert inorder_list(root) == [2, 3, 4, 5, 6, 7, 8]
    assert preorder_list(root) == [5, 3, 2, 4, 7, 6, 8]
    assert is_valid_bst(root)
    assert is_valid_bst_by_inorder(root)

    assert search(root, 6).val == 6
    assert search(root, 10) is None
    assert contains(root, 4)
    assert not contains(root, 10)

    assert leftmost(root).val == 2
    assert rightmost(root).val == 8

    assert floor(root, 5).val == 5
    assert floor(root, 1) is None
    assert ceiling(root, 5).val == 5
    assert ceiling(root, 9) is None
    assert predecessor(root, 5).val == 4
    assert successor(root, 5).val == 6
    assert closest_value(root, 6.2) == 6

    assert lca(root, search(root, 2), search(root, 4)).val == 3
    assert kth_smallest(root, 3) == 4
    assert min_abs_diff(root) == 1
    assert range_sum(root, 4, 7) == 22

    assert inorder_list(trim(clone(root), 3, 7)) == [3, 4, 5, 6, 7]

    left, right = split(clone(root), 5)
    assert inorder_list(left) == [2, 3, 4, 5]
    assert inorder_list(right) == [6, 7, 8]

    assert inorder_list(delete(clone(root), 7)) == [2, 3, 4, 5, 6, 8]

    pre = [8, 5, 1, 7, 10, 12]
    rebuilt = bst_from_preorder(pre)
    assert preorder_list(rebuilt) == pre
    assert verify_preorder(pre)
    assert not verify_preorder([5, 2, 6, 1, 3])

    assert same_tree(deserialize(serialize(root)), root)

    a = bst_from([2, 1, 4])
    b = bst_from([1, 0, 3])
    assert all_elements(a, b) == [0, 1, 1, 2, 3, 4]

    assert two_sum_bst(root, 9)
    assert not two_sum_bst(root, 100)

    assert largest_bst_subtree(root) == 7
    assert max_sum_bst(root) == 35

    sized = None
    for x in [5, 3, 7, 2, 4, 6, 8]:
        sized = sized_insert(sized, x)

    assert rank(sized, 5) == 3
    assert select(sized, 3).key == 5
    assert list(keys_between(sized, 3, 6)) == [3, 4, 5, 6]

    rb = None
    for x in [5, 3, 7, 2, 4, 6, 8]:
        rb = llrb_insert(rb, x)

    assert rb.color is Color.BLACK


if __name__ == "__main__":
    _test()
