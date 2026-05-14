"""
BST Katha Primitives — Simple / Functional Version
==================================================

This file is intentionally Pythonic and LeetCode-friendly.
It does NOT try to mirror Princeton's Java Symbol Table API mechanically.

We use Princeton/Sedgewick for the mental model:
    BST = ordered symbol table
    inorder = sorted stream
    min/max/floor/ceiling/rank/select/range are ordered operations
    LLRB = clean balanced BST via 2-3 tree isomorphism

But the code style stays natural:
    if val < root.val:
        ...
    elif val > root.val:
        ...
    else:
        ...

No compare_key().
No is_left_turn().
No is_right_turn().

A helper earns a name only when it captures a reusable invariant or hides
non-trivial traversal / pointer logic.

Layer map
---------
Level 0 — TreeNode + construction/testing helpers
Level 1 — True atomic BST primitives: leftmost, rightmost
Level 2 — Ordered navigation: search, floor, ceiling, predecessor, successor, LCA
Level 3 — Inorder sorted-stream primitives
Level 4 — Range / mutation / rewiring primitives
Level 5 — Construction / reconstruction / serialization primitives
Level 6 — Multi-BST and arbitrary-tree BST-certificate primitives
Level 7 — Minimal ordered-symbol-table augmentation: rank/select
Level 8 — LLRB awareness primitives
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from enum import Enum
from math import comb
from typing import Iterable, Iterator, Optional


# =============================================================================
# Level 0 — TreeNode + construction/testing helpers
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


def size(root: Optional[TreeNode]) -> int:
    if root is None:
        return 0
    return 1 + size(root.left) + size(root.right)


def height(root: Optional[TreeNode]) -> int:
    """
    Node-count height:
        empty tree  -> 0
        single node -> 1
    """
    if root is None:
        return 0
    return 1 + max(height(root.left), height(root.right))


def insert(root: Optional[TreeNode], val: int) -> TreeNode:
    """
    Plain unbalanced BST insert.

    Composition:
        direct comparison
        recurse into one side
        attach new node at null slot

    LeetCode:
        701. Insert into a Binary Search Tree
        1902. Depth of BST Given Insertion Order, conceptually
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


def same_tree(a: Optional[TreeNode], b: Optional[TreeNode]) -> bool:
    if a is None or b is None:
        return a is b
    return a.val == b.val and same_tree(a.left, b.left) and same_tree(a.right, b.right)


# =============================================================================
# Level 1 — True atomic BST primitives
# =============================================================================


def leftmost(root: TreeNode) -> TreeNode:
    """
    Smallest node in a BST subtree.

    Composition:
        leftmost -> min
        leftmost -> successor when node has right subtree
        leftmost -> replacement node in delete

    LeetCode:
        285. Inorder Successor in BST
        450. Delete Node in a BST
        510. Inorder Successor in BST II
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
# Level 2 — Ordered navigation primitives
# =============================================================================


def search(root: Optional[TreeNode], val: int) -> Optional[TreeNode]:
    """
    Natural BST search.

    Composition:
        direct comparison
        discard one subtree per step

    LeetCode:
        700. Search in a Binary Search Tree
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


def floor(root: Optional[TreeNode], val: int) -> Optional[TreeNode]:
    """
    Largest node with value <= val.

    Mental model:
        root.val <= val -> root is a valid candidate; try right to improve
        root.val >  val -> root too large; go left

    LeetCode:
        270. Closest Binary Search Tree Value
        272. Closest Binary Search Tree Value II
        2476. Closest Nodes Queries in a Binary Search Tree
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
    Strict floor.
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
    Strict ceiling.

    LeetCode:
        285. Inorder Successor in BST
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
    Guided BST search with best-so-far candidate.

    LeetCode:
        270. Closest Binary Search Tree Value
    """
    if root is None:
        raise ValueError("closest_value requires a non-empty BST")

    best = root.val
    while root:
        if abs(root.val - target) < abs(best - target):
            best = root.val
        root = root.left if target < root.val else root.right
    return best


def lca(root: Optional[TreeNode], p: TreeNode, q: TreeNode) -> Optional[TreeNode]:
    """
    Lowest common ancestor in a BST.

    Mental model:
        The answer is the first split point.

    LeetCode:
        235. Lowest Common Ancestor of a Binary Search Tree
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
# Level 3 — Inorder sorted-stream primitives
# =============================================================================


def preorder(root: Optional[TreeNode]) -> Iterator[TreeNode]:
    if root is None:
        return
    yield root
    yield from preorder(root.left)
    yield from preorder(root.right)


def inorder(root: Optional[TreeNode]) -> Iterator[TreeNode]:
    """
    The central BST primitive.

    Invariant:
        If root is a valid BST, inorder(root) emits values in sorted order.

    Composition:
        inorder -> validate / kth / min diff / modes / recover / iterator
        inorder -> merge two BSTs / balance BST / increasing tree / doubly list

    LeetCode:
        98, 99, 173, 230, 426, 501, 530, 783, 897, 1305, 1382, 2476
    """
    if root is None:
        return
    yield from inorder(root.left)
    yield root
    yield from inorder(root.right)


def reverse_inorder(root: Optional[TreeNode]) -> Iterator[TreeNode]:
    """
    Descending sorted stream.

    Composition:
        reverse_inorder + running sum -> greater tree

    LeetCode:
        538. Convert BST to Greater Tree
        1038. Binary Search Tree to Greater Sum Tree
    """
    if root is None:
        return
    yield from reverse_inorder(root.right)
    yield root
    yield from reverse_inorder(root.left)


def inorder_vals(root: Optional[TreeNode]) -> Iterator[int]:
    return (node.val for node in inorder(root))


def preorder_vals(root: Optional[TreeNode]) -> Iterator[int]:
    return (node.val for node in preorder(root))


def inorder_list(root: Optional[TreeNode]) -> list[int]:
    return list(inorder_vals(root))


def preorder_list(root: Optional[TreeNode]) -> list[int]:
    return list(preorder_vals(root))


def is_valid_bst(root: Optional[TreeNode]) -> bool:
    """
    Bounds-based validation.

    Invariant:
        low < node.val < high

    LeetCode:
        98. Validate Binary Search Tree
        1932. Merge BSTs to Create Single BST, final validation idea
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


def is_valid_bst_by_inorder(root: Optional[TreeNode]) -> bool:
    """
    Sorted-stream validation.

    LeetCode:
        98. Validate Binary Search Tree
    """
    prev = None
    for val in inorder_vals(root):
        if prev is not None and val <= prev:
            return False
        prev = val
    return True


def kth_smallest(root: Optional[TreeNode], k: int) -> int:
    """
    Inorder + counter.

    LeetCode:
        230. Kth Smallest Element in a BST
    """
    for i, node in enumerate(inorder(root), start=1):
        if i == k:
            return node.val
    raise ValueError("Tree has fewer than k nodes")


def min_abs_diff(root: Optional[TreeNode]) -> int:
    """
    Minimum difference occurs between adjacent values in sorted order.

    LeetCode:
        530. Minimum Absolute Difference in BST
        783. Minimum Distance Between BST Nodes
    """
    prev = None
    best = float("inf")
    for val in inorder_vals(root):
        if prev is not None:
            best = min(best, val - prev)
        prev = val
    return int(best)


def modes(root: Optional[TreeNode]) -> list[int]:
    """
    Run-length counting over inorder stream.

    LeetCode:
        501. Find Mode in Binary Search Tree
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
    Detect swapped nodes through inorder inversions.

    LeetCode:
        99. Recover Binary Search Tree
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
    Iterative inorder stream.

    Stack invariant:
        stack contains the path to the next smallest unconsumed node.

    LeetCode:
        173. Binary Search Tree Iterator
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
        BSTIterator forward stream
        history list
        index into history

    LeetCode:
        1586. Binary Search Tree Iterator II
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
# Level 4 — Range / mutation / rewiring primitives
# =============================================================================


def range_sum(root: Optional[TreeNode], low: int, high: int) -> int:
    """
    Range pruning.

    LeetCode:
        938. Range Sum of BST
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
    Range pruning + reconnecting.

    LeetCode:
        669. Trim a Binary Search Tree
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
    Split BST into:
        left:  values <= target
        right: values > target

    LeetCode:
        776. Split BST
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
    Delete the leftmost node and return the new subtree root.

    LeetCode:
        450. Delete Node in a BST
    """
    if root.left is None:
        return root.right
    root.left = delete_min(root.left)
    return root


def delete(root: Optional[TreeNode], val: int) -> Optional[TreeNode]:
    """
    Hibbard deletion.

    LeetCode:
        450. Delete Node in a BST
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


def greater_sum_tree(root: Optional[TreeNode]) -> Optional[TreeNode]:
    """
    Reverse inorder accumulation.

    LeetCode:
        538. Convert BST to Greater Tree
        1038. Binary Search Tree to Greater Sum Tree
    """
    total = 0
    for node in reverse_inorder(root):
        total += node.val
        node.val = total
    return root


def increasing_tree(root: Optional[TreeNode]) -> Optional[TreeNode]:
    """
    Rewire BST into a right-only increasing chain.

    LeetCode:
        897. Increasing Order Search Tree
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
    Convert BST to circular sorted doubly linked list.

    Uses:
        left  as prev
        right as next

    LeetCode:
        426. Convert Binary Search Tree to Sorted Doubly Linked List
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
# Level 5 — Construction / reconstruction / serialization primitives
# =============================================================================


def sorted_array_to_bst(nums: list[int]) -> Optional[TreeNode]:
    """
    Median-root balanced construction.

    LeetCode:
        108. Convert Sorted Array to Binary Search Tree
        1382. Balance a Binary Search Tree
    """
    def build(lo: int, hi: int) -> Optional[TreeNode]:
        if lo >= hi:
            return None
        mid = (lo + hi) // 2
        return TreeNode(nums[mid], build(lo, mid), build(mid + 1, hi))

    return build(0, len(nums))


def sorted_list_to_bst(head: Optional[ListNode]) -> Optional[TreeNode]:
    """
    O(n) sorted linked-list to balanced BST.

    Mental model:
        Build the tree in inorder while consuming the list once.

    LeetCode:
        109. Convert Sorted List to Binary Search Tree
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
    Composition:
        inorder values -> sorted_array_to_bst

    LeetCode:
        1382. Balance a Binary Search Tree
    """
    return sorted_array_to_bst(inorder_list(root))


def bst_from_preorder(pre: list[int]) -> Optional[TreeNode]:
    """
    Rebuild BST from preorder using upper bounds.

    LeetCode:
        1008. Construct Binary Search Tree from Preorder Traversal
        449. Serialize and Deserialize BST
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
    Verify preorder sequence of a BST using monotonic stack.

    Invariant:
        lower is the last ancestor whose right subtree we entered.
        Every future value must be > lower.

    LeetCode:
        255. Verify Preorder Sequence in Binary Search Tree
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
    Compact BST serialization with preorder only.

    Why no null markers?
        A general binary tree needs null markers because preorder alone is ambiguous.
        A BST can be reconstructed from preorder using value bounds.

    LeetCode:
        449. Serialize and Deserialize BST
    """
    return SEP.join(str(x) for x in preorder_vals(root))


def deserialize(data: str) -> Optional[TreeNode]:
    if not data:
        return None
    return bst_from_preorder([int(x) for x in data.split(SEP)])


def generate_trees(n: int) -> list[Optional[TreeNode]]:
    """
    Root-split generation.

    LeetCode:
        95. Unique Binary Search Trees II
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
    Catalan DP.

    LeetCode:
        96. Unique Binary Search Trees
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

    LeetCode:
        1569. Number of Ways to Reorder Array to Get Same BST
    """
    def ways(arr: list[int]) -> int:
        if len(arr) <= 2:
            return 1

        root = arr[0]
        left = [x for x in arr[1:] if x < root]
        right = [x for x in arr[1:] if x > root]

        return comb(len(left) + len(right), len(left)) * ways(left) * ways(right) % MOD

    return (ways(nums) - 1) % MOD


# =============================================================================
# Level 6 — Multi-BST and arbitrary-tree BST-certificate primitives
# =============================================================================


def two_sum_bst(root: Optional[TreeNode], target: int) -> bool:
    """
    Inorder scan + set.

    LeetCode:
        653. Two Sum IV - Input is a BST
    """
    seen = set()
    for val in inorder_vals(root):
        if target - val in seen:
            return True
        seen.add(val)
    return False


def two_sum_bsts(a: Optional[TreeNode], b: Optional[TreeNode], target: int) -> bool:
    """
    Hash one BST, scan the other.

    LeetCode:
        1214. Two Sum BSTs
    """
    vals = set(inorder_vals(a))
    return any(target - x in vals for x in inorder_vals(b))


def merge_sorted(a: Iterator[int], b: Iterator[int]) -> Iterator[int]:
    """
    Merge two sorted streams.

    LeetCode:
        1305. All Elements in Two Binary Search Trees
    """
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
    """
    Offline inorder + binary search.

    LeetCode:
        2476. Closest Nodes Queries in a Binary Search Tree
    """
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


@dataclass
class Cert:
    is_bst: bool
    size: int
    min_val: int
    max_val: int
    sum_val: int


EMPTY_CERT = Cert(True, 0, float("inf"), float("-inf"), 0)
BAD_CERT = Cert(False, 0, float("-inf"), float("inf"), 0)


def largest_bst_subtree(root: Optional[TreeNode]) -> int:
    """
    Postorder BST certificate.

    LeetCode:
        333. Largest BST Subtree
    """
    best = 0

    def dfs(node: Optional[TreeNode]) -> Cert:
        nonlocal best
        if node is None:
            return EMPTY_CERT

        left = dfs(node.left)
        right = dfs(node.right)

        if left.is_bst and right.is_bst and left.max_val < node.val < right.min_val:
            curr = Cert(
                True,
                left.size + right.size + 1,
                min(left.min_val, node.val),
                max(right.max_val, node.val),
                left.sum_val + right.sum_val + node.val,
            )
            best = max(best, curr.size)
            return curr

        return BAD_CERT

    dfs(root)
    return best


def max_sum_bst(root: Optional[TreeNode]) -> int:
    """
    Same certificate as largest_bst_subtree, but optimize by sum.

    LeetCode:
        1373. Maximum Sum BST in Binary Tree
    """
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
                True,
                left.size + right.size + 1,
                min(left.min_val, node.val),
                max(right.max_val, node.val),
                total,
            )

        return BAD_CERT

    dfs(root)
    return best


def can_merge(trees: list[TreeNode]) -> Optional[TreeNode]:
    """
    Merge small BSTs into one BST.

    LeetCode:
        1932. Merge BSTs to Create Single BST
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
# Level 7 — Minimal ordered-symbol-table augmentation: rank / select
# =============================================================================

class SizedNode:
    """
    BST node augmented with subtree size.

    This is for Princeton-style ordered-symbol-table operations:
        rank(key): number of keys less than key
        select(k): key with zero-based rank k
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
    """
    Keys in [lo, hi], sorted.
    """
    if root is None:
        return

    if lo < root.key:
        yield from keys_between(root.left, lo, hi)
    if lo <= root.key <= hi:
        yield root.key
    if root.key < hi:
        yield from keys_between(root.right, lo, hi)


# =============================================================================
# Level 8 — LLRB awareness primitives
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
    Compact LLRB insertion repair sequence.

        1. right child red and left child black -> rotate left
        2. left child red and left-left red     -> rotate right
        3. both children red                    -> flip colors
    """
    if is_red(h.right) and not is_red(h.left):
        h = rotate_left(h)

    if is_red(h.left) and is_red(h.left.left):
        h = rotate_right(h)

    if is_red(h.left) and is_red(h.right):
        flip_colors(h)

    return fix_rb_count(h)


def llrb_insert(root: Optional[RBNode], key: int) -> RBNode:
    """
    Balanced BST insertion.

    Composition:
        standard BST insert with new red node
        repair on the way back up
        force root black
    """
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
# Drill map — lower primitives compose into higher problem families
# =============================================================================

DRILL_MAP = """
1. leftmost / rightmost
   -> min/max
   -> successor with right subtree
   -> delete node
   -> 285, 450, 510

2. search
   -> contains / insert / delete path
   -> 700, 701, 450

3. floor / ceiling / predecessor / successor
   -> closest value / closest nodes / successor
   -> 270, 272, 285, 2476

4. inorder
   -> sorted stream
   -> validate / kth / min diff / modes / recover / iterator
   -> 98, 99, 173, 230, 501, 530, 783

5. reverse_inorder
   -> descending stream with running sum
   -> greater tree
   -> 538, 1038

6. range_sum / trim
   -> range pruning
   -> 938, 669

7. split
   -> target partition with reconnecting
   -> 776

8. sorted_array_to_bst / sorted_list_to_bst / balance_bst
   -> sorted sequence to height-balanced BST
   -> 108, 109, 1382

9. bst_from_preorder / verify_preorder / serialize / deserialize
   -> preorder + bounds
   -> 255, 449, 1008

10. merge_sorted over inorder streams
    -> all elements from two BSTs
    -> 1305

11. Cert postorder
    -> identify BST inside arbitrary binary tree
    -> 333, 1373

12. rank / select with subtree sizes
    -> ordered symbol table arsenal
    -> conceptual support for order-statistic BSTs

13. rotate_left / rotate_right / flip_colors
    -> LLRB balanced search tree
    -> balanced BST awareness for interviews
"""


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

    assert floor(root, 5).val == 5
    assert floor(root, 1) is None
    assert ceiling(root, 5).val == 5
    assert ceiling(root, 9) is None
    assert predecessor(root, 5).val == 4
    assert successor(root, 5).val == 6

    assert closest_value(root, 6.2) == 6
    assert kth_smallest(root, 3) == 4
    assert min_abs_diff(root) == 1
    assert range_sum(root, 4, 7) == 22

    assert inorder_list(trim(clone(root), 3, 7)) == [3, 4, 5, 6, 7]

    left, right = split(clone(root), 5)
    assert inorder_list(left) == [2, 3, 4, 5]
    assert inorder_list(right) == [6, 7, 8]

    assert inorder_list(delete(clone(root), 7)) == [2, 3, 4, 5, 6, 8]

    assert inorder_list(sorted_array_to_bst([1, 2, 3, 4, 5])) == [1, 2, 3, 4, 5]
    assert inorder_list(balance_bst(root)) == [2, 3, 4, 5, 6, 7, 8]

    pre = [8, 5, 1, 7, 10, 12]
    rebuilt = bst_from_preorder(pre)
    assert preorder_list(rebuilt) == pre
    assert verify_preorder(pre)
    assert not verify_preorder([5, 2, 6, 1, 3])

    data = serialize(root)
    assert same_tree(deserialize(data), root)

    assert two_sum_bst(root, 9)
    assert not two_sum_bst(root, 100)

    a = bst_from([2, 1, 4])
    b = bst_from([1, 0, 3])
    assert all_elements(a, b) == [0, 1, 1, 2, 3, 4]

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
