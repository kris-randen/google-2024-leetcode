"""
BST Katha — Recursive-First Skeletons, Problem Descriptions, and Solutions
=========================================================================

This file is organized around algorithm skeletons, not around isolated helpers
and not around a detached index.

Each skeleton section contains:
    1. the idea
    2. the LeetCode problems in that family with short descriptions
    3. the primitive composition
    4. the solution functions directly below that skeleton

Policy for style:
    Prefer recursive solutions wherever recursion expresses the BST invariant
    more clearly. Use iterative code only when the problem/API naturally asks
    for pause-resume state, heap state, or stack state.

Core BST superpowers:
    1. Ordered descent: values tell us which subtree to solve.
    2. Sorted projection: inorder traversal turns BST into sorted stream.
    3. Bounds: every subtree lives inside an open interval.
    4. Rewiring: recursive mutation returns the new root of the subtree.
    5. Recurrence: choose/fix root, then recursively solve left and right.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from enum import Enum
from heapq import heappush, heapreplace
from math import comb
from typing import Iterable, Iterator, Optional


# =============================================================================
# 0. Representations and construction helpers
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


class ParentNode:
    """Node shape for LeetCode 510-style successor with parent pointers."""

    def __init__(
        self,
        val: int = 0,
        left: Optional["ParentNode"] = None,
        right: Optional["ParentNode"] = None,
        parent: Optional["ParentNode"] = None,
    ):
        self.val = val
        self.left = left
        self.right = right
        self.parent = parent


def clone(root: Optional[TreeNode]) -> Optional[TreeNode]:
    if root is None:
        return None
    return TreeNode(root.val, clone(root.left), clone(root.right))


def same_tree(a: Optional[TreeNode], b: Optional[TreeNode]) -> bool:
    if a is None or b is None:
        return a is b
    return \
    (
        a.val == b.val and
        same_tree(a.left, b.left) and
        same_tree(a.right, b.right)
    )


def size(root: Optional[TreeNode]) -> int:
    if root is None:
        return 0
    return 1 + size(root.left) + size(root.right)


def height(root: Optional[TreeNode]) -> int:
    if root is None:
        return 0
    return 1 + max(height(root.left), height(root.right))


def list_from(values: Iterable[int]) -> Optional[ListNode]:
    dummy = tail = ListNode()
    for val in values:
        tail.next = ListNode(val)
        tail = tail.next
    return dummy.next


def leftmost(root):
    """
    Smallest node in a BST subtree.

    This stays iterative because the primitive is literally following one chain.
    It composes into min, successor, and delete replacement.
    """
    while root.left:
        root = root.left
    return root


def rightmost(root):
    """Largest node in a BST subtree."""
    while root.right:
        root = root.right
    return root


# =============================================================================
# Skeleton A — Recursive ordered descent
# =============================================================================

SKELETON_A = """
Idea:
    A BST search path is naturally recursive:
        if val < root.val, solve left subtree
        if val > root.val, solve right subtree
        else root is the answer

Problems:

    700. Search in a Binary Search Tree
        Description:
            Return the subtree rooted at val, or None.
        Composition:
            recursive ordered descent

    701. Insert into a Binary Search Tree
        Description:
            Insert val and return root.
        Composition:
            recursive ordered descent + attach at None

    450. Delete Node in a BST
        Description:
            Find and delete key while preserving BST order.
        Composition:
            recursive ordered descent + local rewiring
        Full delete solution is under Skeleton F.
"""


def search_bst(root: Optional[TreeNode], val: int) -> Optional[TreeNode]:
    if root is None:
        return None
    if val < root.val:
        return search_bst(root.left, val)
    if val > root.val:
        return search_bst(root.right, val)
    return root


def insert_into_bst(root: Optional[TreeNode], val: int) -> TreeNode:
    if root is None:
        return TreeNode(val)
    if val < root.val:
        root.left = insert_into_bst(root.left, val)
    elif val > root.val:
        root.right = insert_into_bst(root.right, val)
    return root


def bst_from(values: Iterable[int]) -> Optional[TreeNode]:
    root = None
    for val in values:
        root = insert_into_bst(root, val)
    return root


# =============================================================================
# Skeleton B — Recursive candidate-tracking ordered descent
# =============================================================================

SKELETON_B = """
Idea:
    Some ordered queries need the best candidate seen along the search path.

Problems:

    270. Closest Binary Search Tree Value
        Description:
            Return the value closest to target.
        Composition:
            recursive ordered descent + best-so-far value

    272. Closest Binary Search Tree Value II
        Description:
            Return k values closest to target.
        Composition:
            inorder sorted array + two-pointer expansion around insertion point

    285. Inorder Successor in BST
        Description:
            Return the smallest node greater than p.
        Composition:
            recursive strict ceiling

    510. Inorder Successor in BST II
        Description:
            Successor with parent pointer and no root.
        Composition:
            if right subtree exists -> leftmost(right)
            else climb ancestors

    2476. Closest Nodes Queries in BST
        Description:
            For each query, return floor and ceiling values.
        Composition:
            inorder sorted array + binary search
"""


def floor_node(root: Optional[TreeNode], val: int) -> Optional[TreeNode]:
    """Largest node with value <= val."""
    if root is None:
        return None
    if root.val == val:
        return root
    if root.val > val:
        return floor_node(root.left, val)
    better = floor_node(root.right, val)
    return better or root


def ceiling_node(root: Optional[TreeNode], val: int) -> Optional[TreeNode]:
    """Smallest node with value >= val."""
    if root is None:
        return None
    if root.val == val:
        return root
    if root.val < val:
        return ceiling_node(root.right, val)
    better = ceiling_node(root.left, val)
    return better or root


def predecessor_node(root: Optional[TreeNode], val: int) -> Optional[TreeNode]:
    """Largest node with value < val."""
    if root is None:
        return None
    if root.val >= val:
        return predecessor_node(root.left, val)
    better = predecessor_node(root.right, val)
    return better or root


def successor_node(root: Optional[TreeNode], val: int) -> Optional[TreeNode]:
    """Smallest node with value > val."""
    if root is None:
        return None
    if root.val <= val:
        return successor_node(root.right, val)
    better = successor_node(root.left, val)
    return better or root


def closest_value(root: Optional[TreeNode], target: float) -> int:
    if root is None:
        raise ValueError("closest_value requires non-empty tree")

    def better(a: int, b: int) -> int:
        return a if abs(a - target) <= abs(b - target) else b

    def dfs(node: Optional[TreeNode], best: int) -> int:
        if node is None:
            return best
        best = better(node.val, best)
        return dfs(node.left if target < node.val else node.right, best)

    return dfs(root, root.val)


def closest_k_values(root: Optional[TreeNode], target: float, k: int) -> list[int]:
    """Sorted projection + two-pointer expansion."""
    import bisect

    vals = inorder_list(root)
    right = bisect.bisect_left(vals, target)
    left = right - 1
    ans = []

    while k and (left >= 0 or right < len(vals)):
        if left < 0:
            ans.append(vals[right])
            right += 1
        elif right == len(vals):
            ans.append(vals[left])
            left -= 1
        elif abs(vals[left] - target) <= abs(vals[right] - target):
            ans.append(vals[left])
            left -= 1
        else:
            ans.append(vals[right])
            right += 1
        k -= 1

    return ans


def inorder_successor_bst(root: Optional[TreeNode], p: TreeNode) -> Optional[TreeNode]:
    return successor_node(root, p.val)


def inorder_successor_parent(node: ParentNode) -> Optional[ParentNode]:
    if node.right:
        return leftmost(node.right)
    while node.parent and node is node.parent.right:
        node = node.parent
    return node.parent


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
# Skeleton C — Recursive first split point
# =============================================================================

SKELETON_C = """
Idea:
    For two values p and q, the LCA is the first node where they stop going
    to the same side.

Problem:

    235. Lowest Common Ancestor of a Binary Search Tree
        Description:
            Return the lowest node that has p and q as descendants.
        Composition:
            normalize target interval [lo, hi]
            + recursive ordered descent
            + first node satisfying lo <= root.val <= hi
"""


def lca_bst(root: Optional[TreeNode], p: TreeNode, q: TreeNode) -> Optional[TreeNode]:
    lo = min(p.val, q.val)
    hi = max(p.val, q.val)

    def dfs(node: Optional[TreeNode]) -> Optional[TreeNode]:
        if node is None:
            return None
        if hi < node.val:
            return dfs(node.left)
        if lo > node.val:
            return dfs(node.right)
        return node

    return dfs(root)


# =============================================================================
# Skeleton D — Recursive inorder sorted stream
# =============================================================================

SKELETON_D = """
Idea:
    Recursive inorder is the central BST primitive:
        left -> node -> right
    For a valid BST, this emits values in sorted order.

Problems:

    98. Validate Binary Search Tree
        Description:
            Decide whether tree satisfies BST ordering.
        Composition:
            inorder stream -> strictly increasing check
        Bounds version appears under Skeleton E.

    99. Recover Binary Search Tree
        Description:
            Two nodes are swapped; restore by swapping values back.
        Composition:
            inorder stream -> detect inversions -> swap first/second

    173. Binary Search Tree Iterator
        Description:
            next()/hasNext() ascending iterator.
        Composition:
            explicit stack because API pauses/resumes traversal

    230. Kth Smallest Element in a BST
        Description:
            Return kth smallest.
        Composition:
            recursive inorder stream -> kth emitted node

    501. Find Mode in BST
        Description:
            Return most frequent value(s).
        Composition:
            inorder stream -> equal values form runs -> run-length count

    530 / 783. Minimum Difference / Distance in BST
        Description:
            Return minimum difference between any two node values.
        Composition:
            inorder stream -> adjacent sorted differences

    1586. BST Iterator II
        Description:
            next/prev iterator.
        Composition:
            stack iterator + history array

    3831. Median of a Binary Search Tree Level
        Description:
            Return median value among nodes at a level.
        Composition:
            recursive inorder with depth
            + filter target level
            + median of already-sorted subsequence
"""


def preorder(root: Optional[TreeNode]) -> Iterator[TreeNode]:
    if root is None:
        return
    yield root
    yield from preorder(root.left)
    yield from preorder(root.right)


def inorder(root: Optional[TreeNode]) -> Iterator[TreeNode]:
    if root is None:
        return
    yield from inorder(root.left)
    yield root
    yield from inorder(root.right)


def reverse_inorder(root: Optional[TreeNode]) -> Iterator[TreeNode]:
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


def find_modes(root: Optional[TreeNode]) -> list[int]:
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
    Iterative by necessity: the interface asks traversal to pause/resume.
    """

    def __init__(self, root: Optional[TreeNode]):
        self.stack: list[TreeNode] = []
        self._push_left(root)

    def _push_left(self, root: Optional[TreeNode]) -> None:
        while root:
            self.stack.append(root)
            root = root.left

    def next(self) -> int:
        node = self.stack.pop()
        self._push_left(node.right)
        return node.val

    def hasNext(self) -> bool:
        return bool(self.stack)


class BSTIteratorII:
    """Iterator II is stateful: forward stack iterator + history + index."""

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


def median_at_level(root: Optional[TreeNode], level: int) -> float:
    vals = []

    def dfs(node: Optional[TreeNode], depth: int) -> None:
        if node is None:
            return
        dfs(node.left, depth + 1)
        if depth == level:
            vals.append(node.val)
        dfs(node.right, depth + 1)

    dfs(root, 0)

    if not vals:
        return -1

    mid = len(vals) // 2
    if len(vals) % 2 == 1:
        return vals[mid]
    return (vals[mid - 1] + vals[mid]) / 2


# =============================================================================
# Skeleton E — Recursive bounds
# =============================================================================

SKELETON_E = """
Idea:
    Every subtree has a legal open interval:
        low < node.val < high

Problems:

    98. Validate Binary Search Tree
        Composition:
            recursive DFS + open interval bounds

    1932. Merge BSTs to Create Single BST
        Composition:
            grafting + recursive bounds
        Full solution appears under Skeleton L.
"""


def is_valid_bst(root: Optional[TreeNode]) -> bool:
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
# Skeleton F — Recursive local rewiring
# =============================================================================

SKELETON_F = """
Idea:
    Mutation is clean when each recursive call returns the new root of the
    modified subtree.

Problems:

    450. Delete Node in a BST
        Composition:
            recursive ordered descent + successor replacement + delete_min

    669. Trim a Binary Search Tree
        Composition:
            recursive range pruning + return new root

    776. Split BST
        Composition:
            recursive partition + reconnect child pointer

    897. Increasing Order Search Tree
        Composition:
            recursive inorder stream + tail builder

    426. Convert BST to Sorted Doubly Linked List
        Composition:
            recursive inorder stream + previous/current links

    938. Range Sum of BST
        Composition:
            recursive range pruning without mutation
"""


def range_sum_bst(root: Optional[TreeNode], low: int, high: int) -> int:
    if root is None:
        return 0
    if root.val < low:
        return range_sum_bst(root.right, low, high)
    if root.val > high:
        return range_sum_bst(root.left, low, high)
    return root.val + range_sum_bst(root.left, low, high) + range_sum_bst(root.right, low, high)


def trim_bst(root: Optional[TreeNode], low: int, high: int) -> Optional[TreeNode]:
    if root is None:
        return None
    if root.val < low:
        return trim_bst(root.right, low, high)
    if root.val > high:
        return trim_bst(root.left, low, high)
    root.left = trim_bst(root.left, low, high)
    root.right = trim_bst(root.right, low, high)
    return root


def split_bst(root: Optional[TreeNode], target: int) -> tuple[Optional[TreeNode], Optional[TreeNode]]:
    if root is None:
        return None, None
    if root.val <= target:
        small_from_right, right = split_bst(root.right, target)
        root.right = small_from_right
        return root, right
    left, large_from_left = split_bst(root.left, target)
    root.left = large_from_left
    return left, root


def delete_min(root: TreeNode) -> Optional[TreeNode]:
    if root.left is None:
        return root.right
    root.left = delete_min(root.left)
    return root


def delete_node(root: Optional[TreeNode], key: int) -> Optional[TreeNode]:
    if root is None:
        return None
    if key < root.val:
        root.left = delete_node(root.left, key)
        return root
    if key > root.val:
        root.right = delete_node(root.right, key)
        return root
    if root.left is None:
        return root.right
    if root.right is None:
        return root.left

    nxt = leftmost(root.right)
    nxt.right = delete_min(root.right)
    nxt.left = root.left
    return nxt


def increasing_bst(root: Optional[TreeNode]) -> Optional[TreeNode]:
    dummy = tail = TreeNode()
    for node in inorder(root):
        node.left = None
        tail.right = node
        tail = node
    tail.right = None
    return dummy.right


def tree_to_doubly_list(root: Optional[TreeNode]) -> Optional[TreeNode]:
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
# Skeleton G — Recursive reverse inorder accumulation
# =============================================================================

SKELETON_G = """
Problems:
    538. Convert BST to Greater Tree
    1038. Binary Search Tree to Greater Sum Tree

Composition:
    recursive reverse inorder + running total
"""


def bst_to_gst(root: Optional[TreeNode]) -> Optional[TreeNode]:
    total = 0

    def dfs(node: Optional[TreeNode]) -> None:
        nonlocal total
        if node is None:
            return
        dfs(node.right)
        total += node.val
        node.val = total
        dfs(node.left)

    dfs(root)
    return root


convert_bst = bst_to_gst


# =============================================================================
# Skeleton H — Recursive sorted data -> balanced BST
# =============================================================================

SKELETON_H = """
Problems:
    108. Convert Sorted Array to Binary Search Tree
    109. Convert Sorted List to Binary Search Tree
    1382. Balance a Binary Search Tree

Composition:
    sorted data -> recursive median-root construction
"""


def sorted_array_to_bst(nums: list[int]) -> Optional[TreeNode]:
    def build(lo: int, hi: int) -> Optional[TreeNode]:
        if lo >= hi:
            return None
        mid = (lo + hi) // 2
        return TreeNode(nums[mid], build(lo, mid), build(mid + 1, hi))

    return build(0, len(nums))


def sorted_list_to_bst(head: Optional[ListNode]) -> Optional[TreeNode]:
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
    return sorted_array_to_bst(inorder_list(root))


# =============================================================================
# Skeleton I — Recursive preorder + bounds
# =============================================================================

SKELETON_I = """
Problems:
    255. Verify Preorder Sequence in BST
    449. Serialize and Deserialize BST
    1008. Construct BST from Preorder

Composition:
    preorder consumption + recursive bounds
"""


def bst_from_preorder(preorder: list[int]) -> Optional[TreeNode]:
    i = 0

    def build(low: float, high: float) -> Optional[TreeNode]:
        nonlocal i
        if i == len(preorder) or not (low < preorder[i] < high):
            return None
        val = preorder[i]
        i += 1
        root = TreeNode(val)
        root.left = build(low, val)
        root.right = build(val, high)
        return root

    return build(float("-inf"), float("inf"))


def verify_preorder_recursive(preorder: list[int]) -> bool:
    i = 0

    def consume(low: float, high: float) -> None:
        nonlocal i
        if i == len(preorder) or not (low < preorder[i] < high):
            return
        val = preorder[i]
        i += 1
        consume(low, val)
        consume(val, high)

    consume(float("-inf"), float("inf"))
    return i == len(preorder)


def verify_preorder_stack(preorder: list[int]) -> bool:
    """Canonical monotonic-stack alternative for this specific problem."""
    stack = []
    lower = float("-inf")

    for val in preorder:
        if val <= lower:
            return False
        while stack and val > stack[-1]:
            lower = stack.pop()
        stack.append(val)

    return True


def verify_preorder(preorder: list[int]) -> bool:
    return verify_preorder_recursive(preorder)


SEP = ","


def serialize_bst(root: Optional[TreeNode]) -> str:
    return SEP.join(str(x) for x in preorder_vals(root))


def deserialize_bst(data: str) -> Optional[TreeNode]:
    if not data:
        return None
    return bst_from_preorder([int(x) for x in data.split(SEP)])


class Codec:
    def serialize(self, root: Optional[TreeNode]) -> str:
        return serialize_bst(root)

    def deserialize(self, data: str) -> Optional[TreeNode]:
        return deserialize_bst(data)


# =============================================================================
# Skeleton J — Recursive root-split recurrence
# =============================================================================

SKELETON_J = """
Problems:
    95. Unique Binary Search Trees II
    96. Unique Binary Search Trees
    1569. Number of Ways to Reorder Array to Get Same BST

Composition:
    choose/fix root -> recursively solve left and right -> combine
"""


def generate_trees(n: int) -> list[Optional[TreeNode]]:
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


def num_trees(n: int) -> int:
    memo = {0: 1}

    def count(nodes: int) -> int:
        if nodes in memo:
            return memo[nodes]
        total = 0
        for left_count in range(nodes):
            right_count = nodes - 1 - left_count
            total += count(left_count) * count(right_count)
        memo[nodes] = total
        return total

    return count(n)


MOD = 10**9 + 7


def num_of_ways_same_bst(nums: list[int]) -> int:
    def ways(arr: list[int]) -> int:
        if len(arr) <= 2:
            return 1
        root = arr[0]
        left = [x for x in arr[1:] if x < root]
        right = [x for x in arr[1:] if x > root]
        return (comb(len(left) + len(right), len(left)) * ways(left) * ways(right)) % MOD

    return (ways(nums) - 1) % MOD


# =============================================================================
# Skeleton K — Recursive multi-BST stream/set logic
# =============================================================================

SKELETON_K = """
Problems:
    653. Two Sum IV - Input is a BST
    1214. Two Sum BSTs
    1305. All Elements in Two BSTs

Composition:
    recursive traversal + set, or recursive inorder streams + merge
"""


def find_target(root: Optional[TreeNode], k: int) -> bool:
    seen = set()

    def dfs(node: Optional[TreeNode]) -> bool:
        if node is None:
            return False
        if k - node.val in seen:
            return True
        seen.add(node.val)
        return dfs(node.left) or dfs(node.right)

    return dfs(root)


def two_sum_bsts(a: Optional[TreeNode], b: Optional[TreeNode], target: int) -> bool:
    vals = set(inorder_vals(a))

    def scan(node: Optional[TreeNode]) -> bool:
        if node is None:
            return False
        if target - node.val in vals:
            return True
        return scan(node.left) or scan(node.right)

    return scan(b)


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


def get_all_elements(root1: Optional[TreeNode], root2: Optional[TreeNode]) -> list[int]:
    return list(merge_sorted(inorder_vals(root1), inorder_vals(root2)))


# =============================================================================
# Skeleton L — Recursive postorder BST certificate / forest merge
# =============================================================================

SKELETON_L = """
Problems:
    333. Largest BST Subtree
    1373. Maximum Sum BST in Binary Tree
    1932. Merge BSTs to Create Single BST

Composition:
    postorder certificate, or recursive grafting with bounds
"""


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
# Skeleton M — Augmented ordered tree / streaming order statistic
# =============================================================================

SKELETON_M = """
Problems:
    703. Kth Largest Element in a Stream
    1902. Depth of BST Given Insertion Order

Composition:
    703 uses heap in Python, conceptually dynamic order statistic.
    1902 uses predecessor/successor among existing keys.
"""


class KthLargest:
    def __init__(self, k: int, nums: list[int]):
        self.k = k
        self.heap = []
        for x in nums:
            self.add(x)

    def add(self, val: int) -> int:
        if len(self.heap) < self.k:
            heappush(self.heap, val)
        elif val > self.heap[0]:
            heapreplace(self.heap, val)
        return self.heap[0]


def max_depth_bst_insertion_order(order: list[int]) -> int:
    import bisect

    keys = []
    depth = {}
    best = 0

    for x in order:
        i = bisect.bisect_left(keys, x)
        left_depth = depth[keys[i - 1]] if i > 0 else -1
        right_depth = depth[keys[i]] if i < len(keys) else -1
        depth[x] = 1 + max(left_depth, right_depth)
        best = max(best, depth[x])
        keys.insert(i, x)

    return best


class SizedNode:
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
    if root is None:
        return 0
    if key < root.key:
        return rank(root.left, key)
    if key > root.key:
        return 1 + sized_count(root.left) + rank(root.right, key)
    return sized_count(root.left)


def select(root: Optional[SizedNode], k: int) -> Optional[SizedNode]:
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
# Skeleton N — Recursive LLRB balanced search tree
# =============================================================================

SKELETON_N = """
Idea:
    A left-leaning red-black tree is a BST representation of a 2-3 tree.

Insertion repair:
    1. right red and not left red -> rotate_left
    2. left red and left-left red -> rotate_right
    3. both children red -> flip_colors
"""


class Color(Enum):
    RED = True
    BLACK = False


class RBNode:
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
    x = h.right
    h.right = x.left
    x.left = h
    x.color = h.color
    h.color = Color.RED
    x.count = h.count
    fix_rb_count(h)
    return x


def rotate_right(h: RBNode) -> RBNode:
    x = h.left
    h.left = x.right
    x.right = h
    x.color = h.color
    h.color = Color.RED
    x.count = h.count
    fix_rb_count(h)
    return x


def flip_colors(h: RBNode) -> None:
    h.color = Color.RED if h.color is Color.BLACK else Color.BLACK
    if h.left:
        h.left.color = Color.BLACK if h.left.color is Color.RED else Color.RED
    if h.right:
        h.right.color = Color.BLACK if h.right.color is Color.RED else Color.RED


def balance_llrb(h: RBNode) -> RBNode:
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
# Drill order
# =============================================================================

DRILL_ORDER = [
    "recursive search_bst / insert_into_bst",
    "leftmost / rightmost",
    "recursive floor_node / ceiling_node / predecessor_node / successor_node",
    "recursive closest_value",
    "recursive lca_bst",
    "recursive inorder / reverse_inorder generators",
    "recursive bounds validation",
    "kth_smallest / min_abs_diff / find_modes from inorder",
    "recover_bst from inorder inversions",
    "BSTIterator only where API requires pause/resume",
    "recursive range_sum_bst / trim_bst",
    "recursive delete_node / delete_min",
    "recursive split_bst",
    "recursive reverse-inorder greater-sum tree",
    "recursive sorted_array_to_bst / sorted_list_to_bst / balance_bst",
    "recursive bst_from_preorder / verify_preorder_recursive / Codec",
    "recursive generate_trees / num_trees / num_of_ways_same_bst",
    "recursive find_target / two_sum_bsts / get_all_elements",
    "recursive postorder Cert / largest_bst_subtree / max_sum_bst",
    "recursive grafting can_merge",
    "rank / select / keys_between",
    "recursive llrb_insert with rotations",
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

    assert search_bst(root, 6).val == 6
    assert search_bst(root, 10) is None

    assert leftmost(root).val == 2
    assert rightmost(root).val == 8

    assert floor_node(root, 5).val == 5
    assert floor_node(root, 1) is None
    assert ceiling_node(root, 5).val == 5
    assert ceiling_node(root, 9) is None
    assert predecessor_node(root, 5).val == 4
    assert successor_node(root, 5).val == 6
    assert closest_value(root, 6.2) == 6
    assert sorted(closest_k_values(root, 5.2, 3)) == [4, 5, 6]

    assert lca_bst(root, search_bst(root, 2), search_bst(root, 4)).val == 3
    assert kth_smallest(root, 3) == 4
    assert min_abs_diff(root) == 1
    assert range_sum_bst(root, 4, 7) == 22
    assert median_at_level(root, 2) == 5.0

    assert inorder_list(trim_bst(clone(root), 3, 7)) == [3, 4, 5, 6, 7]

    left, right = split_bst(clone(root), 5)
    assert inorder_list(left) == [2, 3, 4, 5]
    assert inorder_list(right) == [6, 7, 8]

    assert inorder_list(delete_node(clone(root), 7)) == [2, 3, 4, 5, 6, 8]

    pre = [8, 5, 1, 7, 10, 12]
    rebuilt = bst_from_preorder(pre)
    assert preorder_list(rebuilt) == pre
    assert verify_preorder(pre)
    assert verify_preorder_stack(pre)
    assert not verify_preorder([5, 2, 6, 1, 3])
    assert not verify_preorder_stack([5, 2, 6, 1, 3])

    codec = Codec()
    assert same_tree(codec.deserialize(codec.serialize(root)), root)

    assert num_trees(3) == 5
    assert len(generate_trees(3)) == 5

    a = bst_from([2, 1, 4])
    b = bst_from([1, 0, 3])
    assert get_all_elements(a, b) == [0, 1, 1, 2, 3, 4]

    assert find_target(root, 9)
    assert not find_target(root, 100)
    assert two_sum_bsts(a, b, 5)
    assert not two_sum_bsts(a, b, 100)

    assert closest_nodes(root, [1, 5, 9]) == [[-1, 2], [5, 5], [8, -1]]

    assert largest_bst_subtree(root) == 7
    assert max_sum_bst(root) == 35

    kth = KthLargest(3, [4, 5, 8, 2])
    assert kth.add(3) == 4
    assert kth.add(5) == 5

    assert max_depth_bst_insertion_order([2, 1, 4, 3]) == 2

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
