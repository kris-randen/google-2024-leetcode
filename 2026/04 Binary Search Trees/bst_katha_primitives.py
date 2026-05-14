"""
BST Katha Primitive Toolkit
==========================

Purpose
-------
This file is meant to be pasted into a Python file and studied as a layered
Binary Search Tree toolkit.

The design mirrors the Linked List and Pure Binary Tree Katha style:

Level 0: Representation / construction / testing utilities
Level 1: Atomic predicates and child navigation
Level 2: Ordered-symbol-table navigation primitives
Level 3: Inorder sorted-stream primitives
Level 4: Transformation primitives
Level 5: Construction / reconstruction primitives
Level 6: Multi-BST and certificate-DP primitives
Level 7: LLRB balanced-search-tree awareness primitives

Core mental model
-----------------
A Binary Search Tree is a binary tree plus an ordering invariant.

For every node:
    all keys in node.left  are strictly less than node.val
    all keys in node.right are strictly greater than node.val

Because of that invariant:
    inorder traversal emits keys in sorted order
    search can discard half the tree at every comparison
    min is leftmost
    max is rightmost
    floor/ceiling are guided searches
    predecessor/successor are local ordered-symbol-table operations

The Princeton ordered-symbol-table API from Sedgewick maps naturally to BSTs:

    put(key, val)
    get(key)
    delete(key)
    contains(key)
    isEmpty()
    size()
    min()
    max()
    floor(key)
    ceiling(key)
    rank(key)
    select(k)
    deleteMin()
    deleteMax()
    size(lo, hi)
    keys(lo, hi)
    keys()

LeetCode usually gives only TreeNode.val, not key/value pairs or subtree sizes.
So this toolkit includes:
    1. LeetCode-style TreeNode primitives.
    2. Symbol-table style operations where useful.
    3. Size-augmented variants for rank/select.
    4. LLRB primitives as balanced-search-tree awareness.

Exact LeetCode problem family map
---------------------------------

Validation / invariant:
    98. Validate Binary Search Tree

Inorder sorted stream:
    173. Binary Search Tree Iterator
    230. Kth Smallest Element in a BST
    501. Find Mode in Binary Search Tree
    530. Minimum Absolute Difference in BST
    783. Minimum Distance Between BST Nodes
    2476. Closest Nodes Queries in a Binary Search Tree
    3831. Median of a Binary Search Tree Level

Recover / detect swapped nodes:
    99. Recover Binary Search Tree

Search / insert / delete:
    700. Search in a Binary Search Tree
    701. Insert into a Binary Search Tree
    450. Delete Node in a BST

Ordered queries:
    235. Lowest Common Ancestor of a Binary Search Tree
    270. Closest Binary Search Tree Value
    272. Closest Binary Search Tree Value II
    285. Inorder Successor in BST
    510. Inorder Successor in BST II

Range pruning:
    669. Trim a Binary Search Tree
    938. Range Sum of BST

Split / reconnect:
    776. Split BST

Reverse inorder accumulation:
    538. Convert BST to Greater Tree
    1038. Binary Search Tree to Greater Sum Tree

Balanced construction:
    108. Convert Sorted Array to Binary Search Tree
    109. Convert Sorted List to Binary Search Tree
    1382. Balance a Binary Search Tree

BST generation / counting:
    95. Unique Binary Search Trees II
    96. Unique Binary Search Trees
    1569. Number of Ways to Reorder Array to Get Same BST

BST reconstruction / serialization:
    255. Verify Preorder Sequence in Binary Search Tree
    449. Serialize and Deserialize BST
    1008. Construct Binary Search Tree from Preorder Traversal

Two-BST sorted-stream problems:
    1214. Two Sum BSTs
    1305. All Elements in Two Binary Search Trees

BST certificate inside arbitrary binary tree:
    333. Largest BST Subtree
    1373. Maximum Sum BST in Binary Tree

Forest merge:
    1932. Merge BSTs to Create Single BST

BST-to-list / list-to-BST:
    426. Convert Binary Search Tree to Sorted Doubly Linked List
    897. Increasing Order Search Tree

Stream / external balanced tree conceptual:
    703. Kth Largest Element in a Stream
    1902. Depth of BST Given Insertion Order

Note:
    703 is usually solved with a min-heap in Python, not by implementing a BST.
    1902 conceptually benefits from ordered-map / balanced-BST thinking.
"""

from __future__ import annotations

from collections import Counter, defaultdict, deque
from dataclasses import dataclass
from enum import Enum
from math import comb
from typing import Callable, Iterable, Iterator, Optional


# =============================================================================
# Level 0 — Representation / construction / testing utilities
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


def node(val: int, left: Optional[TreeNode] = None, right: Optional[TreeNode] = None) -> TreeNode:
    return TreeNode(val, left, right)


def values_inorder(root: Optional[TreeNode]) -> list[int]:
    return [n.val for n in inorder_nodes(root)]


def values_preorder(root: Optional[TreeNode]) -> list[int]:
    return [n.val for n in preorder_nodes(root)]


def tree_size(root: Optional[TreeNode]) -> int:
    if root is None:
        return 0

    return 1 + tree_size(root.left) + tree_size(root.right)


def tree_height(root: Optional[TreeNode]) -> int:
    """
    Height measured as number of nodes on the longest root-to-leaf path.
    Empty tree has height 0.
    Single-node tree has height 1.
    """
    if root is None:
        return 0

    return 1 + max(tree_height(root.left), tree_height(root.right))


def clone_tree(root: Optional[TreeNode]) -> Optional[TreeNode]:
    if root is None:
        return None

    return TreeNode(
        root.val,
        clone_tree(root.left),
        clone_tree(root.right),
    )


def same_tree(a: Optional[TreeNode], b: Optional[TreeNode]) -> bool:
    if a is None or b is None:
        return a is b

    return (
        a.val == b.val
        and same_tree(a.left, b.left)
        and same_tree(a.right, b.right)
    )


def bst_insert_plain(root: Optional[TreeNode], val: int) -> TreeNode:
    """
    Simple unbalanced BST insert.

    Composition:
        compare key
        branch left/right
        attach leaf at null slot

    LeetCode:
        701. Insert into a Binary Search Tree
        1902. Depth of BST Given Insertion Order, conceptually
    """
    if root is None:
        return TreeNode(val)

    if val < root.val:
        root.left = bst_insert_plain(root.left, val)
    elif val > root.val:
        root.right = bst_insert_plain(root.right, val)

    return root


def bst_from_values(values: Iterable[int]) -> Optional[TreeNode]:
    root = None

    for val in values:
        root = bst_insert_plain(root, val)

    return root


# =============================================================================
# Level 1 — Atomic predicates and child navigation
# =============================================================================

def is_leaf(root: Optional[TreeNode]) -> bool:
    return root is not None and root.left is None and root.right is None


def is_left_turn(root: TreeNode, key: int) -> bool:
    return key < root.val


def is_right_turn(root: TreeNode, key: int) -> bool:
    return key > root.val


def compare_key(root: TreeNode, key: int) -> int:
    """
    Returns:
        -1 if key < root.val
         0 if key == root.val
         1 if key > root.val

    This is the atomic search-direction primitive.
    """
    if key < root.val:
        return -1

    if key > root.val:
        return 1

    return 0


def leftmost(root: TreeNode) -> TreeNode:
    """
    min_node primitive.

    Invariant:
        The smallest key in a BST subtree is reached by following left links.

    LeetCode:
        450. Delete Node in a BST
        285. Inorder Successor in BST
        510. Inorder Successor in BST II
    """
    while root.left:
        root = root.left

    return root


def rightmost(root: TreeNode) -> TreeNode:
    """
    max_node primitive.

    Invariant:
        The largest key in a BST subtree is reached by following right links.
    """
    while root.right:
        root = root.right

    return root


def min_value(root: TreeNode) -> int:
    return leftmost(root).val


def max_value(root: TreeNode) -> int:
    return rightmost(root).val


# =============================================================================
# Level 2 — Core BST navigation primitives
# =============================================================================

def search_bst(root: Optional[TreeNode], key: int) -> Optional[TreeNode]:
    """
    Ordered search.

    Composition:
        compare_key
        discard left or right subtree

    LeetCode:
        700. Search in a Binary Search Tree
        701. Insert into a Binary Search Tree
        450. Delete Node in a BST
    """
    while root:
        cmp = compare_key(root, key)

        if cmp == 0:
            return root

        root = root.left if cmp < 0 else root.right

    return None


def contains_bst(root: Optional[TreeNode], key: int) -> bool:
    return search_bst(root, key) is not None


def lower_bound_node(root: Optional[TreeNode], key: int) -> Optional[TreeNode]:
    """
    First node with value >= key.
    Equivalent to ceiling for exact integer keys.

    Composition:
        candidate tracking
        if node.val >= key, it may be answer; go left to improve
        if node.val < key, go right

    LeetCode:
        270. Closest Binary Search Tree Value
        272. Closest Binary Search Tree Value II
        285. Inorder Successor in BST
        2476. Closest Nodes Queries in a Binary Search Tree
    """
    ans = None

    while root:
        if root.val >= key:
            ans = root
            root = root.left
        else:
            root = root.right

    return ans


def upper_bound_node(root: Optional[TreeNode], key: int) -> Optional[TreeNode]:
    """
    First node with value > key.
    This is strict successor by value.
    """
    ans = None

    while root:
        if root.val > key:
            ans = root
            root = root.left
        else:
            root = root.right

    return ans


def floor_node(root: Optional[TreeNode], key: int) -> Optional[TreeNode]:
    """
    Largest node with value <= key.

    Ordered symbol table primitive:
        floor(key)

    LeetCode:
        270. Closest Binary Search Tree Value
        272. Closest Binary Search Tree Value II
        2476. Closest Nodes Queries in a Binary Search Tree
    """
    ans = None

    while root:
        if root.val <= key:
            ans = root
            root = root.right
        else:
            root = root.left

    return ans


def ceiling_node(root: Optional[TreeNode], key: int) -> Optional[TreeNode]:
    """
    Smallest node with value >= key.

    Ordered symbol table primitive:
        ceiling(key)
    """
    return lower_bound_node(root, key)


def predecessor_node(root: Optional[TreeNode], key: int) -> Optional[TreeNode]:
    """
    Strict predecessor: largest node with value < key.
    """
    ans = None

    while root:
        if root.val < key:
            ans = root
            root = root.right
        else:
            root = root.left

    return ans


def successor_node(root: Optional[TreeNode], key: int) -> Optional[TreeNode]:
    """
    Strict successor: smallest node with value > key.
    """
    return upper_bound_node(root, key)


def closest_value(root: Optional[TreeNode], target: float) -> int:
    """
    Closest value by guided BST search.

    Composition:
        search path
        maintain best candidate by absolute difference

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


def lca_bst(root: Optional[TreeNode], p: TreeNode, q: TreeNode) -> Optional[TreeNode]:
    """
    First split point.

    Mental model:
        If both targets are smaller, LCA is left.
        If both targets are larger, LCA is right.
        Otherwise current node is the split point.

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
# Level 3 — DFS / inorder sorted-stream primitives
# =============================================================================

def preorder_nodes(root: Optional[TreeNode]) -> Iterator[TreeNode]:
    if root is None:
        return

    yield root
    yield from preorder_nodes(root.left)
    yield from preorder_nodes(root.right)


def inorder_nodes(root: Optional[TreeNode]) -> Iterator[TreeNode]:
    """
    BST sorted-stream primitive.

    Invariant:
        In a valid BST, inorder emits nodes in strictly increasing value order.

    LeetCode:
        98. Validate Binary Search Tree
        99. Recover Binary Search Tree
        173. Binary Search Tree Iterator
        230. Kth Smallest Element in a BST
        501. Find Mode in Binary Search Tree
        530. Minimum Absolute Difference in BST
        783. Minimum Distance Between BST Nodes
        1305. All Elements in Two Binary Search Trees
        2476. Closest Nodes Queries in a Binary Search Tree
    """
    if root is None:
        return

    yield from inorder_nodes(root.left)
    yield root
    yield from inorder_nodes(root.right)


def reverse_inorder_nodes(root: Optional[TreeNode]) -> Iterator[TreeNode]:
    """
    Larger keys first.

    LeetCode:
        538. Convert BST to Greater Tree
        1038. Binary Search Tree to Greater Sum Tree
        703. Kth Largest Element in a Stream, conceptually
    """
    if root is None:
        return

    yield from reverse_inorder_nodes(root.right)
    yield root
    yield from reverse_inorder_nodes(root.left)


def inorder_values_iter(root: Optional[TreeNode]) -> Iterator[int]:
    return (node.val for node in inorder_nodes(root))


def is_strictly_increasing(values: Iterable[int]) -> bool:
    it = iter(values)
    prev = next(it, None)

    if prev is None:
        return True

    for val in it:
        if val <= prev:
            return False
        prev = val

    return True


def validate_bst_inorder(root: Optional[TreeNode]) -> bool:
    """
    Validation by sorted-stream invariant.

    LeetCode:
        98. Validate Binary Search Tree
    """
    return is_strictly_increasing(inorder_values_iter(root))


def validate_bst_bounds(
    root: Optional[TreeNode],
    low: Optional[int] = None,
    high: Optional[int] = None,
) -> bool:
    """
    Validation by open interval bounds.

    Invariant:
        Every node must satisfy low < node.val < high.
        Left child gets upper bound node.val.
        Right child gets lower bound node.val.

    LeetCode:
        98. Validate Binary Search Tree
        1932. Merge BSTs to Create Single BST, final validation
    """
    if root is None:
        return True

    if low is not None and root.val <= low:
        return False

    if high is not None and root.val >= high:
        return False

    return (
        validate_bst_bounds(root.left, low, root.val)
        and validate_bst_bounds(root.right, root.val, high)
    )


def kth_smallest(root: Optional[TreeNode], k: int) -> int:
    """
    Inorder + stop at k.

    LeetCode:
        230. Kth Smallest Element in a BST
    """
    if k <= 0:
        raise ValueError("k must be positive")

    for i, node in enumerate(inorder_nodes(root), start=1):
        if i == k:
            return node.val

    raise ValueError("BST has fewer than k nodes")


def min_abs_diff_bst(root: Optional[TreeNode]) -> int:
    """
    Adjacent sorted values have the minimum possible difference.

    LeetCode:
        530. Minimum Absolute Difference in BST
        783. Minimum Distance Between BST Nodes
    """
    prev = None
    best = float("inf")

    for val in inorder_values_iter(root):
        if prev is not None:
            best = min(best, val - prev)
        prev = val

    return int(best)


def find_modes_bst(root: Optional[TreeNode]) -> list[int]:
    """
    Since inorder groups equal values together in a BST that allows duplicates,
    mode can be found by run-length counting.

    LeetCode:
        501. Find Mode in Binary Search Tree

    Note:
        LeetCode's TreeNode examples often imply duplicates can appear.
        This implementation handles duplicates if they occur in inorder runs.
    """
    modes = []
    prev = None
    run = 0
    best = 0

    for val in inorder_values_iter(root):
        if val == prev:
            run += 1
        else:
            prev = val
            run = 1

        if run > best:
            best = run
            modes = [val]
        elif run == best:
            modes.append(val)

    return modes


def recover_bst(root: Optional[TreeNode]) -> None:
    """
    Recover two swapped nodes using inorder inversions.

    Invariant:
        A valid BST has strictly increasing inorder values.
        Swapped nodes create one or two inversions.
        First bad previous node and last bad current node are the swapped pair.

    LeetCode:
        99. Recover Binary Search Tree
    """
    first = second = prev = None

    for curr in inorder_nodes(root):
        if prev is not None and curr.val < prev.val:
            if first is None:
                first = prev
            second = curr
        prev = curr

    if first is not None and second is not None:
        first.val, second.val = second.val, first.val


class BSTIterator:
    """
    Controlled iterative inorder stream.

    Composition:
        push_left_chain
        pop next smallest
        after popping node, push left chain of node.right

    LeetCode:
        173. Binary Search Tree Iterator
        1586. Binary Search Tree Iterator II, as the forward base primitive
    """

    def __init__(self, root: Optional[TreeNode]):
        self.stack: list[TreeNode] = []
        self._push_left(root)

    def _push_left(self, root: Optional[TreeNode]) -> None:
        while root:
            self.stack.append(root)
            root = root.left

    def next(self) -> int:
        if not self.hasNext():
            raise StopIteration

        node = self.stack.pop()
        self._push_left(node.right)
        return node.val

    def hasNext(self) -> bool:
        return bool(self.stack)


class BSTIteratorII:
    """
    Bidirectional iterator.

    Composition:
        BSTIterator forward stream
        history array for values already pulled
        index pointer into history

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
        if not self.hasPrev():
            raise StopIteration

        self.i -= 1
        return self.history[self.i]


# =============================================================================
# Level 4 — Range, pruning, transformation, and rewiring primitives
# =============================================================================

def range_sum_bst(root: Optional[TreeNode], low: int, high: int) -> int:
    """
    Range pruning.

    If root.val < low:
        whole left subtree is too small
    If root.val > high:
        whole right subtree is too large

    LeetCode:
        938. Range Sum of BST
    """
    if root is None:
        return 0

    if root.val < low:
        return range_sum_bst(root.right, low, high)

    if root.val > high:
        return range_sum_bst(root.left, low, high)

    return (
        root.val
        + range_sum_bst(root.left, low, high)
        + range_sum_bst(root.right, low, high)
    )


def trim_bst(root: Optional[TreeNode], low: int, high: int) -> Optional[TreeNode]:
    """
    Reconnect only the valid range.

    LeetCode:
        669. Trim a Binary Search Tree
    """
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
    """
    Split into:
        left_tree:  all nodes <= target
        right_tree: all nodes > target

    Mental model:
        If root.val <= target:
            root belongs to left result.
            Split root.right, then attach the <= part back to root.right.
        Else:
            root belongs to right result.
            Split root.left, then attach the > part back to root.left.

    LeetCode:
        776. Split BST
    """
    if root is None:
        return None, None

    if root.val <= target:
        left_big, right = split_bst(root.right, target)
        root.right = left_big
        return root, right

    left, right_small = split_bst(root.left, target)
    root.left = right_small
    return left, root


def delete_min(root: TreeNode) -> Optional[TreeNode]:
    """
    Delete the minimum node in a BST subtree.

    Ordered symbol table primitive:
        deleteMin()

    LeetCode:
        450. Delete Node in a BST
    """
    if root.left is None:
        return root.right

    root.left = delete_min(root.left)
    return root


def delete_bst(root: Optional[TreeNode], key: int) -> Optional[TreeNode]:
    """
    Hibbard deletion.

    Cases:
        key smaller -> delete from left
        key larger  -> delete from right
        found:
            no left child  -> return right
            no right child -> return left
            two children:
                successor = min(root.right)
                successor.right = delete_min(root.right)
                successor.left = root.left

    LeetCode:
        450. Delete Node in a BST
    """
    if root is None:
        return None

    if key < root.val:
        root.left = delete_bst(root.left, key)
        return root

    if key > root.val:
        root.right = delete_bst(root.right, key)
        return root

    if root.left is None:
        return root.right

    if root.right is None:
        return root.left

    successor = leftmost(root.right)
    successor.right = delete_min(root.right)
    successor.left = root.left
    return successor


def convert_bst_greater_tree(root: Optional[TreeNode]) -> Optional[TreeNode]:
    """
    Reverse inorder accumulation.

    Invariant:
        running_sum contains sum of all keys greater than current node.

    LeetCode:
        538. Convert BST to Greater Tree
        1038. Binary Search Tree to Greater Sum Tree
    """
    running_sum = 0

    for node in reverse_inorder_nodes(root):
        running_sum += node.val
        node.val = running_sum

    return root


def increasing_bst(root: Optional[TreeNode]) -> Optional[TreeNode]:
    """
    Rewire BST into increasing right-only chain.

    Composition:
        inorder sorted stream
        detach left
        append to right chain

    LeetCode:
        897. Increasing Order Search Tree
    """
    dummy = tail = TreeNode(0)

    for node in inorder_nodes(root):
        node.left = None
        tail.right = node
        tail = node

    tail.right = None
    return dummy.right


def bst_to_doubly_list(root: Optional[TreeNode]) -> Optional[TreeNode]:
    """
    Convert BST to circular sorted doubly linked list.
    Uses TreeNode.left as prev and TreeNode.right as next.

    Composition:
        inorder sorted stream
        link previous <-> current
        close circular list

    LeetCode:
        426. Convert Binary Search Tree to Sorted Doubly Linked List
    """
    if root is None:
        return None

    first = last = None

    for curr in inorder_nodes(root):
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
        return TreeNode(
            nums[mid],
            build(lo, mid),
            build(mid + 1, hi),
        )

    return build(0, len(nums))


class ListNode:
    def __init__(self, val: int = 0, next: Optional["ListNode"] = None):
        self.val = val
        self.next = next


def sorted_list_to_bst_slow_fast(head: Optional[ListNode]) -> Optional[TreeNode]:
    """
    Split linked list around middle.

    Composition:
        slow/fast middle
        cut before middle
        recursively build left/right

    LeetCode:
        109. Convert Sorted List to Binary Search Tree
    """
    if head is None:
        return None

    if head.next is None:
        return TreeNode(head.val)

    prev = None
    slow = fast = head

    while fast and fast.next:
        prev = slow
        slow = slow.next
        fast = fast.next.next

    prev.next = None

    root = TreeNode(slow.val)
    root.left = sorted_list_to_bst_slow_fast(head)
    root.right = sorted_list_to_bst_slow_fast(slow.next)
    return root


def sorted_list_to_bst_inorder(head: Optional[ListNode]) -> Optional[TreeNode]:
    """
    O(n) construction from sorted linked list.

    Mental model:
        The list is consumed in inorder.
        First build left subtree of size n//2.
        Current list node becomes root.
        Then build right subtree.

    LeetCode:
        109. Convert Sorted List to Binary Search Tree
    """
    n = 0
    curr = head

    while curr:
        n += 1
        curr = curr.next

    curr = head

    def build(size: int) -> Optional[TreeNode]:
        nonlocal curr

        if size == 0:
            return None

        left = build(size // 2)

        root = TreeNode(curr.val)
        root.left = left
        curr = curr.next

        root.right = build(size - size // 2 - 1)
        return root

    return build(n)


def balance_bst(root: Optional[TreeNode]) -> Optional[TreeNode]:
    """
    Composition:
        inorder sorted values
        sorted_array_to_bst

    LeetCode:
        1382. Balance a Binary Search Tree
    """
    return sorted_array_to_bst(list(inorder_values_iter(root)))


def bst_from_preorder_bounds(preorder: list[int]) -> Optional[TreeNode]:
    """
    Construct BST from preorder using upper bound.

    Mental model:
        Preorder gives root before children.
        BST bounds tell whether the next value belongs in this subtree.

    LeetCode:
        1008. Construct Binary Search Tree from Preorder Traversal
        449. Serialize and Deserialize BST
    """
    i = 0

    def build(bound: float) -> Optional[TreeNode]:
        nonlocal i

        if i == len(preorder) or preorder[i] > bound:
            return None

        val = preorder[i]
        i += 1

        root = TreeNode(val)
        root.left = build(val)
        root.right = build(bound)
        return root

    return build(float("inf"))


def verify_preorder_bst(preorder: list[int]) -> bool:
    """
    Verify preorder sequence using monotonic stack.

    Invariant:
        lower_bound is the last ancestor for which we moved into the right subtree.
        Any future value must be greater than lower_bound.

    LeetCode:
        255. Verify Preorder Sequence in Binary Search Tree
    """
    stack = []
    lower = float("-inf")

    for val in preorder:
        if val <= lower:
            return False

        while stack and val > stack[-1]:
            lower = stack.pop()

        stack.append(val)

    return True


SEP = ","

def serialize_bst_preorder(root: Optional[TreeNode]) -> str:
    """
    Compact BST serialization.

    Why compact?
        For a general binary tree, preorder alone is ambiguous unless null markers
        are included. For a BST, preorder plus value bounds is enough to rebuild.

    LeetCode:
        449. Serialize and Deserialize BST
    """
    return SEP.join(str(v) for v in values_preorder(root))


def deserialize_bst_preorder(data: str) -> Optional[TreeNode]:
    if not data:
        return None

    preorder = [int(x) for x in data.split(SEP)]
    return bst_from_preorder_bounds(preorder)


def generate_trees(n: int) -> list[Optional[TreeNode]]:
    """
    Generate all structurally unique BSTs storing values 1..n.

    Root-split recurrence:
        choose root r
        recursively generate all left trees from [lo, r)
        recursively generate all right trees from (r, hi]
        cartesian product

    LeetCode:
        95. Unique Binary Search Trees II
    """

    def build(lo: int, hi: int) -> list[Optional[TreeNode]]:
        if lo > hi:
            return [None]

        ans = []

        for r in range(lo, hi + 1):
            for left in build(lo, r - 1):
                for right in build(r + 1, hi):
                    ans.append(TreeNode(r, left, right))

        return ans

    return build(1, n)


def num_trees(n: int) -> int:
    """
    Catalan DP.

    LeetCode:
        96. Unique Binary Search Trees
    """
    dp = [0] * (n + 1)
    dp[0] = 1

    for size in range(1, n + 1):
        for left_size in range(size):
            right_size = size - 1 - left_size
            dp[size] += dp[left_size] * dp[right_size]

    return dp[n]


def num_trees_catalan(n: int) -> int:
    return comb(2 * n, n) // (n + 1)


MOD = 10**9 + 7

def num_of_ways_same_bst(nums: list[int]) -> int:
    """
    Count reorderings that produce the same BST.

    Recurrence:
        root = nums[0]
        left  = values < root
        right = values > root
        interleave left/right sequences while preserving their internal relative order

    LeetCode:
        1569. Number of Ways to Reorder Array to Get Same BST
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
# Level 6 — Multi-BST streams and certificate-DP primitives
# =============================================================================

def merge_sorted_iter(a: Iterator[int], b: Iterator[int]) -> Iterator[int]:
    """
    Merge two increasing value streams.

    LeetCode:
        1305. All Elements in Two Binary Search Trees
    """
    va = next(a, None)
    vb = next(b, None)

    while va is not None and vb is not None:
        if va <= vb:
            yield va
            va = next(a, None)
        else:
            yield vb
            vb = next(b, None)

    while va is not None:
        yield va
        va = next(a, None)

    while vb is not None:
        yield vb
        vb = next(b, None)


def get_all_elements(root1: Optional[TreeNode], root2: Optional[TreeNode]) -> list[int]:
    """
    Composition:
        inorder_values_iter(root1)
        inorder_values_iter(root2)
        merge_sorted_iter

    LeetCode:
        1305. All Elements in Two Binary Search Trees
    """
    return list(merge_sorted_iter(inorder_values_iter(root1), inorder_values_iter(root2)))


def two_sum_bsts(root1: Optional[TreeNode], root2: Optional[TreeNode], target: int) -> bool:
    """
    Hash + DFS version.

    LeetCode:
        1214. Two Sum BSTs

    Alternative:
        Use two sorted streams, one ascending and one descending.
    """
    seen = set(inorder_values_iter(root1))

    return any(target - val in seen for val in inorder_values_iter(root2))


def closest_nodes_queries(root: Optional[TreeNode], queries: list[int]) -> list[list[int]]:
    """
    Offline sorted-array + binary search solution.

    LeetCode:
        2476. Closest Nodes Queries in a Binary Search Tree
    """
    import bisect

    vals = list(inorder_values_iter(root))
    ans = []

    for q in queries:
        i = bisect.bisect_left(vals, q)

        floor = vals[i - 1] if i > 0 else -1
        ceil = vals[i] if i < len(vals) else -1

        if i < len(vals) and vals[i] == q:
            floor = ceil = q

        ans.append([floor, ceil])

    return ans


@dataclass
class BSTInfo:
    is_bst: bool
    size: int
    min_val: int
    max_val: int
    sum_val: int


EMPTY_BST_INFO = BSTInfo(
    is_bst=True,
    size=0,
    min_val=float("inf"),
    max_val=float("-inf"),
    sum_val=0,
)


def largest_bst_subtree(root: Optional[TreeNode]) -> int:
    """
    Postorder BST certificate.

    For each subtree return:
        is_bst
        size
        min_val
        max_val

    Parent is BST iff:
        left is BST
        right is BST
        left.max < root.val < right.min

    LeetCode:
        333. Largest BST Subtree
    """
    best = 0

    def dfs(node: Optional[TreeNode]) -> BSTInfo:
        nonlocal best

        if node is None:
            return EMPTY_BST_INFO

        left = dfs(node.left)
        right = dfs(node.right)

        if left.is_bst and right.is_bst and left.max_val < node.val < right.min_val:
            info = BSTInfo(
                is_bst=True,
                size=left.size + right.size + 1,
                min_val=min(left.min_val, node.val),
                max_val=max(right.max_val, node.val),
                sum_val=left.sum_val + right.sum_val + node.val,
            )
            best = max(best, info.size)
            return info

        return BSTInfo(
            is_bst=False,
            size=0,
            min_val=float("-inf"),
            max_val=float("inf"),
            sum_val=0,
        )

    dfs(root)
    return best


def max_sum_bst(root: Optional[TreeNode]) -> int:
    """
    Same certificate as largest_bst_subtree, but optimize by sum.

    LeetCode:
        1373. Maximum Sum BST in Binary Tree
    """
    best = 0

    def dfs(node: Optional[TreeNode]) -> BSTInfo:
        nonlocal best

        if node is None:
            return EMPTY_BST_INFO

        left = dfs(node.left)
        right = dfs(node.right)

        if left.is_bst and right.is_bst and left.max_val < node.val < right.min_val:
            total = left.sum_val + right.sum_val + node.val
            best = max(best, total)

            return BSTInfo(
                is_bst=True,
                size=left.size + right.size + 1,
                min_val=min(left.min_val, node.val),
                max_val=max(right.max_val, node.val),
                sum_val=total,
            )

        return BSTInfo(
            is_bst=False,
            size=0,
            min_val=float("-inf"),
            max_val=float("inf"),
            sum_val=0,
        )

    dfs(root)
    return best


def can_merge_bsts(trees: list[TreeNode]) -> Optional[TreeNode]:
    """
    Leaf-root grafting + final validation.

    LeetCode:
        1932. Merge BSTs to Create Single BST

    High-level composition:
        map root values to trees
        count leaves
        choose unique root not appearing as a leaf
        DFS-graft matching leaf values
        final bounds validation and node-count validation
    """
    roots = {t.val: t for t in trees}
    leaf_count = Counter()

    for t in trees:
        if t.left:
            leaf_count[t.left.val] += 1
        if t.right:
            leaf_count[t.right.val] += 1

    candidates = [t for t in trees if leaf_count[t.val] == 0]

    if len(candidates) != 1:
        return None

    root = candidates[0]
    used = set()

    def graft(curr: Optional[TreeNode], low: int, high: int) -> bool:
        if curr is None:
            return True

        if not (low < curr.val < high):
            return False

        if curr.left is None and curr.right is None and curr.val in roots and curr is not roots[curr.val]:
            other = roots[curr.val]
            curr.left = other.left
            curr.right = other.right
            used.add(curr.val)

        return graft(curr.left, low, curr.val) and graft(curr.right, curr.val, high)

    used.add(root.val)

    if not graft(root, float("-inf"), float("inf")):
        return None

    if len(used) != len(trees):
        return None

    return root


# =============================================================================
# Level 7 — Size-augmented ordered-symbol-table primitives
# =============================================================================

class OSTNode:
    """
    Ordered Symbol Table BST node with subtree size.

    This is not the default LeetCode TreeNode, but it explains Princeton's
    ordered symbol table operations:

        rank(key): number of keys less than key
        select(k): key of rank k
        size(lo, hi): number of keys in range
    """

    def __init__(
        self,
        key: int,
        val: int = 0,
        left: Optional["OSTNode"] = None,
        right: Optional["OSTNode"] = None,
        size: int = 1,
    ):
        self.key = key
        self.val = val
        self.left = left
        self.right = right
        self.size = size


def ost_size(root: Optional[OSTNode]) -> int:
    return root.size if root else 0


def ost_fix_size(root: OSTNode) -> OSTNode:
    root.size = 1 + ost_size(root.left) + ost_size(root.right)
    return root


def ost_put(root: Optional[OSTNode], key: int, val: int) -> OSTNode:
    if root is None:
        return OSTNode(key, val)

    if key < root.key:
        root.left = ost_put(root.left, key, val)
    elif key > root.key:
        root.right = ost_put(root.right, key, val)
    else:
        root.val = val

    return ost_fix_size(root)


def ost_rank(root: Optional[OSTNode], key: int) -> int:
    """
    Number of keys less than key.

    Ordered symbol table primitive:
        rank(key)

    Composition:
        if key < root.key:
            rank is in left subtree
        if key > root.key:
            left size + root + rank in right subtree
        if equal:
            left size
    """
    if root is None:
        return 0

    if key < root.key:
        return ost_rank(root.left, key)

    if key > root.key:
        return 1 + ost_size(root.left) + ost_rank(root.right, key)

    return ost_size(root.left)


def ost_select(root: Optional[OSTNode], k: int) -> Optional[OSTNode]:
    """
    Node with rank k, zero-indexed.

    Ordered symbol table primitive:
        select(k)
    """
    if root is None:
        return None

    left_size = ost_size(root.left)

    if k < left_size:
        return ost_select(root.left, k)

    if k > left_size:
        return ost_select(root.right, k - left_size - 1)

    return root


def ost_range_size(root: Optional[OSTNode], lo: int, hi: int) -> int:
    """
    Number of keys in [lo, hi].
    """
    if root is None or lo > hi:
        return 0

    return ost_rank(root, hi + 1) - ost_rank(root, lo)


def ost_keys(root: Optional[OSTNode], lo: int, hi: int) -> Iterator[int]:
    """
    Keys in [lo, hi] in sorted order.

    Ordered symbol table primitive:
        keys(lo, hi)
    """
    if root is None:
        return

    if lo < root.key:
        yield from ost_keys(root.left, lo, hi)

    if lo <= root.key <= hi:
        yield root.key

    if root.key < hi:
        yield from ost_keys(root.right, lo, hi)


# =============================================================================
# Level 8 — LLRB balanced-search-tree primitives
# =============================================================================

class Color(Enum):
    RED = True
    BLACK = False


class LLRBNode:
    """
    Left-Leaning Red-Black node.

    Important representation choice:
        The color stored in a node represents the color of the link from its
        parent to this node.

    Null links are black.

    2-3 tree isomorphism:
        black links connect 2-nodes / 3-nodes
        red left links glue two BST nodes into one 3-node
        red links must lean left
    """

    def __init__(
        self,
        key: int,
        val: int = 0,
        color: Color = Color.RED,
        left: Optional["LLRBNode"] = None,
        right: Optional["LLRBNode"] = None,
        size: int = 1,
    ):
        self.key = key
        self.val = val
        self.color = color
        self.left = left
        self.right = right
        self.size = size


def llrb_is_red(root: Optional[LLRBNode]) -> bool:
    """
    Null links are black.
    """
    return root is not None and root.color is Color.RED


def llrb_size(root: Optional[LLRBNode]) -> int:
    return root.size if root else 0


def llrb_fix_size(root: LLRBNode) -> LLRBNode:
    root.size = 1 + llrb_size(root.left) + llrb_size(root.right)
    return root


def rotate_left(h: LLRBNode) -> LLRBNode:
    """
    Orient a temporarily right-leaning red link to lean left.

    Before:
            h
             \
              x(red)
             /
            beta

    After:
            x
           /
          h(red)
           \
            beta

    Used when:
        is_red(h.right) and not is_red(h.left)

    Princeton/Sedgewick primitive:
        rotateLeft
    """
    x = h.right
    h.right = x.left
    x.left = h

    x.color = h.color
    h.color = Color.RED

    x.size = h.size
    llrb_fix_size(h)

    return x


def rotate_right(h: LLRBNode) -> LLRBNode:
    """
    Balance two consecutive left red links.

    Before:
            h
           /
          x(red)
         /
        a(red)

    After:
            x
           / \
          a   h(red)

    Used when:
        is_red(h.left) and is_red(h.left.left)

    Princeton/Sedgewick primitive:
        rotateRight
    """
    x = h.left
    h.left = x.right
    x.right = h

    x.color = h.color
    h.color = Color.RED

    x.size = h.size
    llrb_fix_size(h)

    return x


def flip_colors(h: LLRBNode) -> None:
    """
    Split a temporary 4-node.

    Before:
        h is black, both children red

    After:
        h becomes red, children become black

    Princeton/Sedgewick primitive:
        flipColors
    """
    h.color = Color.RED if h.color is Color.BLACK else Color.BLACK

    if h.left:
        h.left.color = Color.BLACK if h.left.color is Color.RED else Color.RED

    if h.right:
        h.right.color = Color.BLACK if h.right.color is Color.RED else Color.RED


def llrb_balance(h: LLRBNode) -> LLRBNode:
    """
    The beautifully small LLRB repair sequence.

    Same code handles the insertion cases:
        1. Right child red, left child black: rotate left.
        2. Left child red and left-left grandchild red: rotate right.
        3. Both children red: flip colors.

    This is the compact Sedgewick LLRB algorithm.
    """
    if llrb_is_red(h.right) and not llrb_is_red(h.left):
        h = rotate_left(h)

    if llrb_is_red(h.left) and llrb_is_red(h.left.left):
        h = rotate_right(h)

    if llrb_is_red(h.left) and llrb_is_red(h.right):
        flip_colors(h)

    return llrb_fix_size(h)


def llrb_put(root: Optional[LLRBNode], key: int, val: int = 0) -> LLRBNode:
    """
    Balanced symbol-table insertion.

    Composition:
        standard BST insert, new node red
        repair on way back up with:
            rotate_left
            rotate_right
            flip_colors
        force root black

    Interview explanation:
        This maintains a 1-1 correspondence with a 2-3 tree.
    """

    def put(h: Optional[LLRBNode], key: int, val: int) -> LLRBNode:
        if h is None:
            return LLRBNode(key, val, Color.RED)

        if key < h.key:
            h.left = put(h.left, key, val)
        elif key > h.key:
            h.right = put(h.right, key, val)
        else:
            h.val = val

        return llrb_balance(h)

    root = put(root, key, val)
    root.color = Color.BLACK
    return root


# =============================================================================
# Drill order
# =============================================================================

BST_KATHA_DRILL_ORDER = [
    "compare_key / search_bst",
    "leftmost / rightmost",
    "floor_node / ceiling_node / predecessor_node / successor_node",
    "validate_bst_bounds",
    "inorder_nodes as sorted stream",
    "kth_smallest",
    "min_abs_diff_bst",
    "recover_bst",
    "BSTIterator",
    "range_sum_bst / trim_bst",
    "delete_min / delete_bst",
    "split_bst",
    "reverse_inorder_nodes / convert_bst_greater_tree",
    "sorted_array_to_bst",
    "sorted_list_to_bst_inorder",
    "bst_from_preorder_bounds",
    "serialize_bst_preorder / deserialize_bst_preorder",
    "merge_sorted_iter / get_all_elements",
    "BSTInfo certificate DP",
    "ost_rank / ost_select",
    "LLRB rotate_left / rotate_right / flip_colors / llrb_put",
]


# =============================================================================
# Small smoke tests
# =============================================================================

def _smoke_test() -> None:
    root = bst_from_values([5, 3, 7, 2, 4, 6, 8])

    assert values_inorder(root) == [2, 3, 4, 5, 6, 7, 8]
    assert validate_bst_bounds(root)
    assert validate_bst_inorder(root)
    assert search_bst(root, 6).val == 6
    assert floor_node(root, 5).val == 5
    assert floor_node(root, 1) is None
    assert ceiling_node(root, 5).val == 5
    assert ceiling_node(root, 9) is None
    assert predecessor_node(root, 5).val == 4
    assert successor_node(root, 5).val == 6
    assert kth_smallest(root, 3) == 4
    assert min_abs_diff_bst(root) == 1
    assert range_sum_bst(root, 4, 7) == 22
    assert values_inorder(trim_bst(clone_tree(root), 3, 7)) == [3, 4, 5, 6, 7]

    left, right = split_bst(clone_tree(root), 5)
    assert values_inorder(left) == [2, 3, 4, 5]
    assert values_inorder(right) == [6, 7, 8]

    balanced = sorted_array_to_bst([1, 2, 3, 4, 5])
    assert validate_bst_bounds(balanced)
    assert values_inorder(balanced) == [1, 2, 3, 4, 5]

    pre = [8, 5, 1, 7, 10, 12]
    rebuilt = bst_from_preorder_bounds(pre)
    assert values_preorder(rebuilt) == pre
    assert verify_preorder_bst(pre)
    assert not verify_preorder_bst([5, 2, 6, 1, 3])

    data = serialize_bst_preorder(root)
    assert same_tree(deserialize_bst_preorder(data), root)

    assert list(get_all_elements(
        bst_from_values([2, 1, 4]),
        bst_from_values([1, 0, 3]),
    )) == [0, 1, 1, 2, 3, 4]

    ost = None
    for k in [5, 3, 7, 2, 4, 6, 8]:
        ost = ost_put(ost, k, k)

    assert ost_rank(ost, 5) == 3
    assert ost_select(ost, 3).key == 5
    assert list(ost_keys(ost, 3, 6)) == [3, 4, 5, 6]

    rb = None
    for k in [5, 3, 7, 2, 4, 6, 8]:
        rb = llrb_put(rb, k, k)

    assert rb.color is Color.BLACK


if __name__ == "__main__":
    _smoke_test()
