"""
Pure Binary Tree Primitive Toolkit

This file is converted from the original markdown notes into a Python-friendly
module. Explanatory prose is kept as comments, while reusable primitives and
example compositions are kept as executable Python definitions.
"""

from __future__ import annotations

# Yes. Here is the redone Part 2A — Pure Binary Tree Primitive Toolkit, with both:
#
# 1. actual reusable code primitives
# 2. clear explanation of what each primitive is and why it matters

#
# Scope: this is still Pure Binary Tree only. It intentionally excludes BST-order primitives, construction/serialization, graph-converted trees, and deeper Tree DP. The attached problem list includes the relevant pure binary-tree problems such as traversal, same/symmetric tree, level order, path sums, flattening, next-right pointers, right-side view, invert tree, LCA, vertical order, width, pruning, completeness, boundary, and flip-equivalence problems.
#
# ------------------------------------------------------------------------
#
# Part 2A — Pure Binary Tree Primitive Toolkit
#
# 0. Core Representation + Atomic Predicates
#
from collections import deque, defaultdict
from typing import Optional, Iterator, Callable, Any


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


def is_leaf(node: Optional[TreeNode]) -> bool:
    return node is not None and node.left is None and node.right is None


def children(node: TreeNode) -> Iterator[TreeNode]:
    if node.left:
        yield node.left
    if node.right:
        yield node.right

#
# What this primitive is
#
# This is the atomic vocabulary of binary-tree work:
#
# node is None        -> absent subtree
# node is leaf        -> real node with no children
# node.left/right     -> child pointers
# children(node)      -> non-null children only

#
# Why it is important
#
# A huge number of binary-tree bugs come from confusing:
#
# None

#
# with:
#
# leaf node

#
# They are not the same.
#
# For example, in Minimum Depth of Binary Tree, this tree:
#
# 1
#  \
#   2

#
# has minimum depth 2, not 1.
#
# Why? Because the missing left child is not a leaf. A valid root-to-leaf path must end at a real node.
#
# Problems it helps with
#
# 111. Minimum Depth of Binary Tree
# 112. Path Sum
# 113. Path Sum II
# 129. Sum Root to Leaf Numbers
# 257. Binary Tree Paths
# 404. Sum of Left Leaves
# 872. Leaf-Similar Trees

#
# Mental invariant
#
# Only real nodes can terminate root-to-leaf logic.
# None only means "there is no subtree here."

#
# This one tiny predicate is worth drilling because it prevents many wrong recursive base cases.
#
# ------------------------------------------------------------------------
#
# 1. Recursive DFS Traversal Primitives
#
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

#
# Example wrappers:
#

def preorder_values(root: Optional[TreeNode]) -> list[int]:
    return [node.val for node in preorder_nodes(root)]


def inorder_values(root: Optional[TreeNode]) -> list[int]:
    return [node.val for node in inorder_nodes(root)]


def postorder_values(root: Optional[TreeNode]) -> list[int]:
    return [node.val for node in postorder_nodes(root)]

#
# What this primitive is
#
# This gives you the three canonical DFS orders:
#
# preorder:   node -> left -> right
# inorder:    left -> node -> right
# postorder:  left -> right -> node

#
# Why it is important
#
# These are not just traversal problems. They are the grammar of tree recursion.
#
# Each order has a natural use:
#
# preorder:
#     parent is processed before children
#     useful when state flows downward
#
# inorder:
#     left-root-right order
#     plain traversal in normal binary trees
#     sorted stream in BSTs, but that is for the BST toolkit
#
# postorder:
#     children are processed before parent
#     useful when parent needs child results

#
# Problems it helps with
#
# Directly:
#
# 94. Binary Tree Inorder Traversal
# 144. Binary Tree Preorder Traversal
# 145. Binary Tree Postorder Traversal

#
# Indirectly:
#
# 112. Path Sum
# 113. Path Sum II
# 129. Sum Root to Leaf Numbers
# 226. Invert Binary Tree
# 617. Merge Two Binary Trees
# 814. Binary Tree Pruning

#
# Mental invariant
#
# The question to ask is:
#
# Do I need to process the current node before or after its children?

#
# If before, think preorder.
# If after, think postorder.
# If left-root-right ordering matters, think inorder.
#
# Trap
#
# Do not say “DFS” vaguely. Say exactly which DFS:
#
# preorder DFS
# inorder DFS
# postorder DFS

#
# Those are different primitives.
#
# ------------------------------------------------------------------------
#
# 2. Iterative DFS Traversal Primitives
#
def preorder_iter(root: Optional[TreeNode]) -> Iterator[TreeNode]:
    if root is None:
        return

    stack = [root]

    while stack:
        node = stack.pop()
        yield node

        if node.right:
            stack.append(node.right)
        if node.left:
            stack.append(node.left)


def inorder_iter(root: Optional[TreeNode]) -> Iterator[TreeNode]:
    stack = []
    node = root

    while stack or node:
        while node:
            stack.append(node)
            node = node.left

        node = stack.pop()
        yield node
        node = node.right


def postorder_iter(root: Optional[TreeNode]) -> Iterator[TreeNode]:
    if root is None:
        return

    stack = [(root, False)]

    while stack:
        node, visited = stack.pop()

        if visited:
            yield node
        else:
            stack.append((node, True))

            if node.right:
                stack.append((node.right, False))
            if node.left:
                stack.append((node.left, False))

#
# What this primitive is
#
# This is the explicit-stack version of recursive traversal.
#
# You are manually simulating the call stack.
#
# Why it is important
#
# Recursive DFS is elegant, but interviewers sometimes ask for iterative traversal. More importantly, iterative traversal teaches you the underlying control flow.
#
# There are three different stack ideas here:
#
# preorder_iter:
#     stack of future nodes to process
#
# inorder_iter:
#     walk-left stack
#
# postorder_iter:
#     two-phase frame using visited marker

#
# Problems it helps with
#
# Directly:
#
# 94. Binary Tree Inorder Traversal
# 144. Binary Tree Preorder Traversal
# 145. Binary Tree Postorder Traversal

#
# Later, the same ideas help with:
#
# 173. BST Iterator
# 230. Kth Smallest Element in a BST

#
# Those are BST problems, but they reuse the iterative inorder primitive.
#
# Mental invariant
#
# For iterative traversal, always ask:
#
# What does each stack frame represent?

#
# For postorder:
#
# (node, False) means children have not been processed.
# (node, True) means children are done; now emit node.

#
# That visited-marker pattern is very important for harder tree problems.
#
# ------------------------------------------------------------------------
#
# 3. BFS Level Frame Primitive
#

def level_nodes(root: Optional[TreeNode]) -> Iterator[list[TreeNode]]:
    if root is None:
        return

    q = deque([root])

    while q:
        level_size = len(q)
        level = []

        for _ in range(level_size):
            node = q.popleft()
            level.append(node)

            if node.left:
                q.append(node.left)
            if node.right:
                q.append(node.right)

        yield level


def level_values(root: Optional[TreeNode]) -> list[list[int]]:
    return [[node.val for node in level] for level in level_nodes(root)]

#
# Example compositions:
#
def right_side_view(root: Optional[TreeNode]) -> list[int]:
    return [level[-1].val for level in level_nodes(root)]


def largest_values_by_level(root: Optional[TreeNode]) -> list[int]:
    return [max(node.val for node in level) for level in level_nodes(root)]


def average_values_by_level(root: Optional[TreeNode]) -> list[float]:
    return [
        sum(node.val for node in level) / len(level)
        for level in level_nodes(root)
    ]

#
# What this primitive is
#
# This is not just “BFS.”
#
# This is:
#
# BFS + level boundary

#
# At the start of every outer loop, the queue contains exactly one level of the tree.
#
# Why it is important
#
# Many tree problems are level problems disguised as traversal problems.
#
# The real primitive is:
#
# capture level_size
# process exactly that many nodes
# enqueue children for next level

#
# That level_size snapshot is the key.
#
# Problems it helps with
#
# 102. Binary Tree Level Order Traversal
# 103. Binary Tree Zigzag Level Order Traversal
# 107. Binary Tree Level Order Traversal II
# 199. Binary Tree Right Side View
# 513. Find Bottom Left Tree Value
# 515. Find Largest Value in Each Tree Row
# 637. Average of Levels in Binary Tree
# 116. Populating Next Right Pointers in Each Node
# 117. Populating Next Right Pointers in Each Node II

#
# Mental invariant
#
# At the beginning of each outer loop iteration,
# q contains exactly the nodes of the current level.

#
# Trap
#
# Do not let the current level and next level blur together.
#
# This is safe:
#
# level_size = len(q)
# for _ in range(level_size):
#     ...

#
# This is bug-prone:
#
# for node in q:
#     ...

#
# because q is being mutated.
#
# ------------------------------------------------------------------------
#
# 4. DFS With Depth Primitive
#
def preorder_with_depth(
    root: Optional[TreeNode],
    *,
    right_first: bool = False,
) -> Iterator[tuple[TreeNode, int]]:
    def dfs(node: Optional[TreeNode], depth: int) -> Iterator[tuple[TreeNode, int]]:
        if node is None:
            return

        yield node, depth

        first = node.right if right_first else node.left
        second = node.left if right_first else node.right

        yield from dfs(first, depth + 1)
        yield from dfs(second, depth + 1)

    yield from dfs(root, 0)

#
# Example compositions:
#
def right_view_dfs(root: Optional[TreeNode]) -> list[int]:
    view = []

    for node, depth in preorder_with_depth(root, right_first=True):
        if depth == len(view):
            view.append(node.val)

    return view


def left_view_dfs(root: Optional[TreeNode]) -> list[int]:
    view = []

    for node, depth in preorder_with_depth(root, right_first=False):
        if depth == len(view):
            view.append(node.val)

    return view


def max_depth(root: Optional[TreeNode]) -> int:
    if root is None:
        return 0

    return max(depth for _, depth in preorder_with_depth(root)) + 1

#
# What this primitive is
#
# This is DFS where every node is paired with its depth:
#
# (node, depth)

#
# Depth becomes part of the traversal state.
#
# Why it is important
#
# Many problems depend not only on the node but also on where the node appears vertically.
#
# This primitive lets you solve view problems without BFS.
#
# Problems it helps with
#
# 104. Maximum Depth of Binary Tree
# 199. Binary Tree Right Side View
# 513. Find Bottom Left Tree Value

#
# It also prepares you for:
#
# 314. Vertical Order Traversal
# 662. Maximum Width of Binary Tree
# 865. Smallest Subtree with all Deepest Nodes

#
# Mental invariant
#
# For right side view:
#
# right-first DFS
# + first node seen at each depth
# = visible node from right side

#
# For left side view:
#
# left-first DFS
# + first node seen at each depth
# = visible node from left side

#
# Trap
#
# The child traversal order matters.
#
# This:
#
# right first + first seen

#
# is not the same as:
#
# left first + overwrite later

#
# Both can work, but they are different invariants. Name the one you are using.
#
# ------------------------------------------------------------------------
#
# 5. Root-to-Leaf Path Primitive
#
def root_to_leaf_paths(root: Optional[TreeNode]) -> Iterator[list[TreeNode]]:
    path = []

    def dfs(node: Optional[TreeNode]) -> Iterator[list[TreeNode]]:
        if node is None:
            return

        path.append(node)

        if is_leaf(node):
            yield path.copy()
        else:
            yield from dfs(node.left)
            yield from dfs(node.right)

        path.pop()

    yield from dfs(root)

#
# Example compositions:
#
def has_path_sum(root: Optional[TreeNode], target: int) -> bool:
    return any(
        sum(node.val for node in path) == target
        for path in root_to_leaf_paths(root)
    )


def path_sum_paths(root: Optional[TreeNode], target: int) -> list[list[int]]:
    return [
        [node.val for node in path]
        for path in root_to_leaf_paths(root)
        if sum(node.val for node in path) == target
    ]


def binary_tree_paths(root: Optional[TreeNode]) -> list[str]:
    return [
        "->".join(str(node.val) for node in path)
        for path in root_to_leaf_paths(root)
    ]


def leaf_values(root: Optional[TreeNode]) -> list[int]:
    return [path[-1].val for path in root_to_leaf_paths(root)]

#
# What this primitive is
#
# This emits every complete root-to-leaf path.
#
# A path is only emitted when it reaches a leaf.
#
# Why it is important
#
# This is one of the most reusable pure binary-tree primitives because many problems ask you to reason about complete paths, not arbitrary prefixes.
#
# Problems it helps with
#
# 112. Path Sum
# 113. Path Sum II
# 129. Sum Root to Leaf Numbers
# 257. Binary Tree Paths
# 872. Leaf-Similar Trees

#
# Mental invariant
#
# path always contains exactly the nodes from root to current node.

#
# Before leaving a recursive call, the path must be restored.
#
# That is why this line matters:
#
# path.pop()

#
# Trap
#
# This reusable version is beautiful and testable, but sometimes not asymptotically ideal because it materializes paths.
#
# For interviews, use it to understand the reduction. Then optimize by carrying only the state needed, such as current sum or current number.
#
# That optimized form is the next primitive.
#
# ------------------------------------------------------------------------
#
# 6. Downward Accumulator DFS Primitive
#
def dfs_down(
    root: Optional[TreeNode],
    initial_state: Any,
    update: Callable[[Any, TreeNode], Any],
    on_leaf: Callable[[Any, TreeNode], Any],
) -> list[Any]:
    results = []

    def dfs(node: Optional[TreeNode], state: Any) -> None:
        if node is None:
            return

        new_state = update(state, node)

        if is_leaf(node):
            results.append(on_leaf(new_state, node))
            return

        dfs(node.left, new_state)
        dfs(node.right, new_state)

    dfs(root, initial_state)
    return results

#
# Example compositions:
#
def has_path_sum_fast(root: Optional[TreeNode], target: int) -> bool:
    sums = dfs_down(
        root,
        0,
        update=lambda acc, node: acc + node.val,
        on_leaf=lambda acc, node: acc,
    )

    return target in sums


def sum_root_to_leaf_numbers(root: Optional[TreeNode]) -> int:
    nums = dfs_down(
        root,
        0,
        update=lambda acc, node: acc * 10 + node.val,
        on_leaf=lambda acc, node: acc,
    )

    return sum(nums)

#
# A more direct left-leaf version:
#
def sum_of_left_leaves(root: Optional[TreeNode]) -> int:
    total = 0

    def dfs(node: Optional[TreeNode], is_left: bool) -> None:
        nonlocal total

        if node is None:
            return

        if is_leaf(node) and is_left:
            total += node.val
            return

        dfs(node.left, True)
        dfs(node.right, False)

    dfs(root, False)
    return total

#
# What this primitive is
#
# This is DFS where a piece of state flows from parent to child.
#
# Examples of downward state:
#
# current sum
# remaining sum
# current root-to-node number
# current path string
# whether this node is a left child
# current depth
# expected preorder index

#
# Why it is important
#
# This is the cleanest primitive for problems where the parent context determines how the child should be interpreted.
#
# You are not asking:
#
# What does this subtree return upward?

#
# You are asking:
#
# Given the state so far, what state should the child receive?

#
# Problems it helps with
#
# 112. Path Sum
# 113. Path Sum II
# 129. Sum Root to Leaf Numbers
# 257. Binary Tree Paths
# 404. Sum of Left Leaves
# 971. Flip Binary Tree To Match Preorder Traversal

#
# Mental invariant
#
# new_state = update(parent_state, current_node)

#
# Then that new_state is passed to children.
#
# Trap
#
# There are two broad variants:
#
# immutable state:
#     pass new_state down
#
# mutable state:
#     mutate before recursion, undo after recursion

#
# Mutable state is efficient but bug-prone. The invariant must be:
#
# After dfs(node) returns, caller-visible state is restored.

#
# ------------------------------------------------------------------------
#
# 7. Pairwise Structural Recursion Primitive
#
# Same-tree pairing
#
def same_tree(a: Optional[TreeNode], b: Optional[TreeNode]) -> bool:
    if a is None or b is None:
        return a is b

    return (
        a.val == b.val
        and same_tree(a.left, b.left)
        and same_tree(a.right, b.right)
    )

#
# Mirror pairing
#
def mirror_equal(a: Optional[TreeNode], b: Optional[TreeNode]) -> bool:
    if a is None or b is None:
        return a is b

    return (
        a.val == b.val
        and mirror_equal(a.left, b.right)
        and mirror_equal(a.right, b.left)
    )


def is_symmetric(root: Optional[TreeNode]) -> bool:
    return root is None or mirror_equal(root.left, root.right)

#
# Flip-equivalent pairing
#
def flip_equivalent(a: Optional[TreeNode], b: Optional[TreeNode]) -> bool:
    if a is None or b is None:
        return a is b

    if a.val != b.val:
        return False

    same_orientation = (
        flip_equivalent(a.left, b.left)
        and flip_equivalent(a.right, b.right)
    )

    flipped_orientation = (
        flip_equivalent(a.left, b.right)
        and flip_equivalent(a.right, b.left)
    )

    return same_orientation or flipped_orientation

#
# What this primitive is
#
# This is recursion over two nodes at a time.
#
# The primitive is not simply “DFS.” It is:
#
# two-node recursive relation
# + child-pairing rule

#
# Why it is important
#
# A lot of tree comparison problems are solved by picking the correct child-pairing relation.
#
# There are three major pairings:
#
# same-direction:
#     a.left  with b.left
#     a.right with b.right
#
# mirror-direction:
#     a.left  with b.right
#     a.right with b.left
#
# flip-allowed:
#     either same-direction works
#     or mirror-direction works

#
# Problems it helps with
#
# 100. Same Tree
# 101. Symmetric Tree
# 572. Subtree of Another Tree
# 617. Merge Two Binary Trees
# 951. Flip Equivalent Binary Trees

#
# Mental invariant
#
# For same_tree:
#
# Two subtrees are same if:
# 1. roots are both null, or
# 2. roots are both non-null with equal values,
# 3. left subtrees are same,
# 4. right subtrees are same.

#
# For symmetry:
#
# Two subtrees mirror each other if:
# 1. roots match,
# 2. outside children mirror,
# 3. inside children mirror.

#
# Trap
#
# For symmetry, the comparison is not:
#
# left.left with right.left

#
# It is:
#
# left.left  with right.right
# left.right with right.left

#
# For flip equivalence, avoid greedy flipping unless the values force it. The safe primitive checks both orientations.
#
# ------------------------------------------------------------------------
#
# 8. Zipped Tree Traversal / Merge Primitive
#
def zip_trees(
    a: Optional[TreeNode],
    b: Optional[TreeNode],
    combine: Callable[[int, int], int],
) -> Optional[TreeNode]:
    if a is None:
        return b

    if b is None:
        return a

    a.val = combine(a.val, b.val)
    a.left = zip_trees(a.left, b.left, combine)
    a.right = zip_trees(a.right, b.right, combine)

    return a


def merge_trees(a: Optional[TreeNode], b: Optional[TreeNode]) -> Optional[TreeNode]:
    return zip_trees(a, b, lambda x, y: x + y)

#
# What this primitive is
#
# This is pairwise traversal where corresponding nodes are combined, not merely compared.
#
# It is the tree equivalent of zipping two lists.
#
# Why it is important
#
# It separates the shape logic from the value logic.
#
# The shape logic says:
#
# if one side is missing, use the other side
# if both exist, combine them and recurse

#
# The value logic says:
#
# new value = combine(a.val, b.val)

#
# Problems it helps with
#
# 617. Merge Two Binary Trees

#
# It also conceptually supports comparison problems like Same Tree, though those use different null semantics.
#
# Mental invariant
#
# The result tree preserves the union of both input shapes.
# Where both trees have nodes, their values are combined.

#
# Trap
#
# Notice the null semantics differ from same_tree.
#
# For same_tree:
#
# one null + one non-null = false

#
# For merge_trees:
#
# one null + one non-null = keep the non-null subtree

#
# Same traversal shape. Different base-case meaning.
#
# ------------------------------------------------------------------------
#
# 9. Positional BFS Primitive
#
def bfs_with_position(
    root: Optional[TreeNode],
) -> Iterator[tuple[TreeNode, int, int, int]]:
    """
    Yields:
        node, depth, column, heap_index

    column:
        left  = col - 1
        right = col + 1

    heap_index:
        left  = 2 * i
        right = 2 * i + 1
    """
    if root is None:
        return

    q = deque([(root, 0, 0, 0)])

    while q:
        node, depth, col, idx = q.popleft()
        yield node, depth, col, idx

        if node.left:
            q.append((node.left, depth + 1, col - 1, 2 * idx))

        if node.right:
            q.append((node.right, depth + 1, col + 1, 2 * idx + 1))

#
# Example composition:
#

def vertical_order(root: Optional[TreeNode]) -> list[list[int]]:
    cols = defaultdict(list)

    for node, _, col, _ in bfs_with_position(root):
        cols[col].append(node.val)

    return [cols[c] for c in sorted(cols)]

#
# What this primitive is
#
# This is BFS where every node carries positional metadata:
#
# depth
# column
# heap-style index

#
# Why it is important
#
# Some problems are not really about tree recursion. They are about projecting the tree into a coordinate system.
#
# Examples:
#
# vertical order:
#     column changes left/right
#
# maximum width:
#     heap-style index measures gaps
#
# print tree:
#     row/column position determines output placement

#
# Problems it helps with
#
# 314. Binary Tree Vertical Order Traversal
# 655. Print Binary Tree
# 662. Maximum Width of Binary Tree

#
# Mental invariant
#
# left child:
#     depth + 1
#     column - 1
#     heap_index = 2 * i
#
# right child:
#     depth + 1
#     column + 1
#     heap_index = 2 * i + 1

#
# Trap
#
# For vertical order, BFS order matters if the problem expects top-to-bottom ordering within each column.
#
# For width, raw heap indices can grow very large. For that, use the safer specialized primitive below.
#
# ------------------------------------------------------------------------
#
# 10. Indexed-Level Width Primitive
#
def indexed_levels(root: Optional[TreeNode]) -> Iterator[list[tuple[TreeNode, int]]]:
    if root is None:
        return

    q = deque([(root, 0)])

    while q:
        level_size = len(q)
        base = q[0][1]
        level = []

        for _ in range(level_size):
            node, idx = q.popleft()
            idx -= base
            level.append((node, idx))

            if node.left:
                q.append((node.left, 2 * idx))

            if node.right:
                q.append((node.right, 2 * idx + 1))

        yield level


def max_width(root: Optional[TreeNode]) -> int:
    best = 0

    for level in indexed_levels(root):
        best = max(best, level[-1][1] - level[0][1] + 1)

    return best

#
# What this primitive is
#
# This is the specialized version of positional BFS for width problems.
#
# It tracks the index a node would have if the tree were stored like a heap array.
#
# Why it is important
#
# The width of a binary tree includes gaps between nodes.
#
# For example:
#
#         1
#        / \
#       2   3
#      /     \
#     4       7

#
# The bottom level width is not 2. It is 4, because the missing positions between 4 and 7 count.
#
# Problems it helps with
#
# 662. Maximum Width of Binary Tree

#
# Conceptually related to:
#
# 958. Check Completeness of a Binary Tree
# 919. Complete Binary Tree Inserter
# 222. Count Complete Tree Nodes

#
# Mental invariant
#
# At each level:
#
# width = rightmost_index - leftmost_index + 1

#
# The normalization step:
#
# idx -= base

#
# keeps indices small.
#
# Trap
#
# If you use raw heap indices without normalization, indices can grow exponentially with depth. Python handles big integers, but the normalized version is conceptually cleaner and portable.
#
# ------------------------------------------------------------------------
#
# 11. Completeness / Null-Slot BFS Primitive
#
def is_complete_tree(root: Optional[TreeNode]) -> bool:
    if root is None:
        return True

    q = deque([root])
    seen_null_slot = False

    while q:
        node = q.popleft()

        if node is None:
            seen_null_slot = True
            continue

        if seen_null_slot:
            return False

        q.append(node.left)
        q.append(node.right)

    return True

#
# What this primitive is
#
# This is BFS over child slots, not just real nodes.
#
# That distinction matters.
#
# Why it is important
#
# A complete binary tree fills levels left to right. Therefore:
#
# In level-order slot traversal,
# after the first missing slot appears,
# no real node may appear later.

#
# Problems it helps with
#
# 958. Check Completeness of a Binary Tree
# 919. Complete Binary Tree Inserter
# 222. Count Complete Tree Nodes

#
# Mental invariant
#
# Once seen_null_slot is True,
# every later popped slot must also be None.

#
# Trap
#
# Do not skip None children too early.
#
# This is wrong for completeness checking:
#
# if node.left:
#     q.append(node.left)
# if node.right:
#     q.append(node.right)

#
# Why? Because the missing slots are exactly the evidence needed to detect incompleteness.
#
# For completeness, enqueue both:
#
# q.append(node.left)
# q.append(node.right)

#
# even if they are None.
#
# ------------------------------------------------------------------------
#
# 12. Local Mutation Primitives
#
def swap_children(node: TreeNode) -> None:
    node.left, node.right = node.right, node.left


def invert_tree(root: Optional[TreeNode]) -> Optional[TreeNode]:
    if root is None:
        return None

    swap_children(root)
    invert_tree(root.left)
    invert_tree(root.right)

    return root

#
# Add-row helpers:
#
def insert_children_under(node: TreeNode, val: int) -> None:
    old_left = node.left
    old_right = node.right

    node.left = TreeNode(val, old_left, None)
    node.right = TreeNode(val, None, old_right)


def add_one_row(
    root: Optional[TreeNode],
    val: int,
    depth: int,
) -> Optional[TreeNode]:
    if depth == 1:
        return TreeNode(val, root, None)

    for level_depth, level in enumerate(level_nodes(root), start=1):
        if level_depth == depth - 1:
            for node in level:
                insert_children_under(node, val)
            break

    return root

#
# What this primitive is
#
# This is controlled pointer mutation in a tree.
#
# The basic operations are:
#
# swap children
# save old child
# replace child
# attach old child under new node

#
# Why it is important
#
# Mutation problems are where many candidates lose subtrees accidentally.
#
# The core discipline is:
#
# Before overwriting a child pointer, ask:
# Do I still need the old subtree?

#
# Problems it helps with
#
# 226. Invert Binary Tree
# 623. Add One Row to Tree
# 617. Merge Two Binary Trees
# 971. Flip Binary Tree To Match Preorder Traversal
# 114. Flatten Binary Tree to Linked List

#
# Mental invariant
#
# For insert_children_under:
#
# old left subtree becomes left child of new left node
# old right subtree becomes right child of new right node

#
# So:
#
# node.left = new node
# node.right = new node

#
# but the old subtrees are not lost.
#
# Trap
#
# This is dangerous:
#
# node.left = TreeNode(val)
# node.left.left = node.left

#
# because after overwriting node.left, you no longer have access to the original left child.
#
# Always save first:
#
# old_left = node.left

#
# ------------------------------------------------------------------------
#
# 13. Flatten / Preorder Rewiring Primitive
#
def flatten_preorder_right_chain(root: Optional[TreeNode]) -> None:
    prev = None

    def dfs(node: Optional[TreeNode]) -> None:
        nonlocal prev

        if node is None:
            return

        dfs(node.right)
        dfs(node.left)

        node.right = prev
        node.left = None
        prev = node

    dfs(root)

#
# What this primitive is
#
# This rewires a binary tree into a right-only linked list following preorder order.
#
# But the traversal used is reverse preorder:
#
# right -> left -> node

#
# Why it is important
#
# Flattening is a classic example where normal traversal intuition can destroy the tree if you mutate too early.
#
# Reverse preorder makes it elegant:
#
# Maintain prev as the already-flattened suffix.
# Attach current node before prev.

#
# Problems it helps with
#
# 114. Flatten Binary Tree to Linked List

#
# The deeper primitive also helps with pointer-rewiring discipline generally.
#
# Mental invariant
#
# Before processing node:
#
# prev points to the flattened chain of all nodes that should come after node.

#
# After processing node:
#
# node.right = prev
# node.left = None
# prev = node

#
# Trap
#
# The naive preorder approach often does this:
#
# process node
# overwrite node.right
# then lose original node.right subtree

#
# Reverse preorder avoids that because both children are processed before rewiring the current node.
#
# ------------------------------------------------------------------------
#
# 14. Boundary Decomposition Primitive
#
def boundary_of_binary_tree(root: Optional[TreeNode]) -> list[int]:
    if root is None:
        return []

    if is_leaf(root):
        return [root.val]

    def left_boundary(node: Optional[TreeNode]) -> list[int]:
        result = []

        while node:
            if not is_leaf(node):
                result.append(node.val)

            node = node.left if node.left else node.right

        return result

    def leaves(node: Optional[TreeNode]) -> list[int]:
        if node is None:
            return []

        if is_leaf(node):
            return [node.val]

        return leaves(node.left) + leaves(node.right)

    def right_boundary(node: Optional[TreeNode]) -> list[int]:
        result = []

        while node:
            if not is_leaf(node):
                result.append(node.val)

            node = node.right if node.right else node.left

        return result[::-1]

    return (
        [root.val]
        + left_boundary(root.left)
        + leaves(root.left)
        + leaves(root.right)
        + right_boundary(root.right)
    )

#
# What this primitive is
#
# Boundary traversal is not one traversal. It is a decomposition:
#
# root
# + left boundary excluding leaves
# + all leaves left to right
# + right boundary excluding leaves, reversed

#
# Why it is important
#
# This teaches an important skill: sometimes a tree problem is not solved by picking one traversal order. Sometimes it must be decomposed into semantic regions.
#
# Problems it helps with
#
# 545. Boundary of Binary Tree

#
# Mental invariant
#
# Leaves are collected exactly once.
# Boundary walks exclude leaves.

#
# Trap
#
# The most common bug is duplication:
#
# root duplicated as leaf
# left boundary leaf duplicated
# right boundary leaf duplicated

#
# The clean rule is:
#
# Only the leaf collector emits leaves.
# Boundary collectors skip leaves.

#
# ------------------------------------------------------------------------
#
# 15. Primitive Ranking for Part 2A
#
# | Rank | Primitive                                            | Why it is high ROI                                          |
# | ---: | ---------------------------------------------------- | ----------------------------------------------------------- |
# |    1 | is_leaf                                            | Prevents the most common base-case bugs.                    |
# |    2 | level_nodes                                        | Unlocks almost every BFS/view/level aggregation problem.    |
# |    3 | preorder_nodes, inorder_nodes, postorder_nodes | Core traversal grammar.                                     |
# |    4 | dfs_down                                           | Unlocks path-sum, root-to-leaf, accumulated-state problems. |
# |    5 | root_to_leaf_paths                                 | Cleanest conceptual primitive for path enumeration.         |
# |    6 | same_tree, mirror_equal, flip_equivalent       | Captures structural-comparison family precisely.            |
# |    7 | preorder_with_depth                                | Enables DFS-based views and depth-indexed reasoning.        |
# |    8 | bfs_with_position                                  | Unlocks vertical/width/layout-style problems.               |
# |    9 | indexed_levels                                     | Specialized high-value primitive for width.                 |
# |   10 | is_complete_tree                                   | Captures complete-tree slot invariant.                      |
# |   11 | swap_children, insert_children_under             | Mutation safety primitives.                                 |
# |   12 | flatten_preorder_right_chain                       | Teaches advanced pointer rewiring.                          |
# |   13 | boundary_of_binary_tree                            | Specialized but useful decomposition pattern.               |
#
# ------------------------------------------------------------------------
#
# 16. Composition Chains
#
# Chain A — Root-to-leaf problems
#
# is_leaf
# + preorder/downward DFS
# + path or accumulator state
# → root-to-leaf evaluator
# → 112, 113, 129, 257

#
# Examples:
#
# 112 Path Sum:
#     state = current sum
#
# 113 Path Sum II:
#     state = current path + current sum
#
# 129 Sum Root to Leaf Numbers:
#     state = current number
#
# 257 Binary Tree Paths:
#     state = current path string/list

#
# ------------------------------------------------------------------------
#
# Chain B — Level-order problems
#
# queue
# + fixed level_size snapshot
# + per-level emission/aggregation
# → BFS level frame
# → 102, 103, 107, 199, 515, 637

#
# Examples:
#
# 102:
#     emit all levels
#
# 103:
#     emit level reversed on alternating parity
#
# 199:
#     take last node of each level
#
# 515:
#     max over level
#
# 637:
#     average over level

#
# ------------------------------------------------------------------------
#
# Chain C — Structural comparison problems
#
# two-node recursion
# + node compatibility
# + child-pairing rule
# → structural relation
# → 100, 101, 951

#
# Variants:
#
# 100 Same Tree:
#     same-direction pairing
#
# 101 Symmetric Tree:
#     mirror-direction pairing
#
# 951 Flip Equivalent:
#     same-direction OR mirror-direction pairing

#
# ------------------------------------------------------------------------
#
# Chain D — Geometry problems
#
# BFS traversal
# + positional metadata
# + grouped aggregation
# → geometry/view problem
# → 314, 655, 662

#
# Examples:
#
# 314 Vertical Order:
#     group by column
#
# 662 Maximum Width:
#     track heap-style index
#
# 655 Print Tree:
#     place node by row/column span

#
# ------------------------------------------------------------------------
#
# Chain E — Mutation problems
#
# tree traversal
# + save old child pointers
# + local rewiring
# → structural transformation
# → 226, 623, 114, 617, 971

#
# The universal mutation question:
#
# Am I about to overwrite a subtree I still need?

#
# ------------------------------------------------------------------------
#
# 17. The Actual Part 2A Toolkit To Drill
#
# If you want the short drilling checklist, drill these in order:
#
# 1. is_leaf
# 2. preorder_nodes / inorder_nodes / postorder_nodes
# 3. preorder_iter / inorder_iter / postorder_iter
# 4. level_nodes
# 5. preorder_with_depth
# 6. root_to_leaf_paths
# 7. dfs_down
# 8. same_tree / mirror_equal / flip_equivalent
# 9. zip_trees
# 10. bfs_with_position
# 11. indexed_levels
# 12. is_complete_tree
# 13. swap_children / insert_children_under
# 14. flatten_preorder_right_chain
# 15. boundary_of_binary_tree

#
# This is now a real toolkit: concrete primitives, named precisely, with the reason each one exists.
