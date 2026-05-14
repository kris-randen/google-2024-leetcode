"""
Binary Tree Iteration Primitives Practice Module

This file is intentionally written as a Python module, not as markdown.
You should be able to paste it into a .py file and run python -m py_compile on it.

Scope
-----
This module focuses only on iteration-style binary-tree primitives:

1. Node streams
   Tree -> Iterator[TreeNode]
   Examples: preorder, inorder, postorder.

2. Value streams
   Tree -> Iterator[int]
   Examples: inorder values, preorder values.

3. Level streams
   Tree -> Iterator[list[TreeNode]]
   Examples: level order, zigzag level order, right side view, level sums.

4. Annotated streams
   Tree -> Iterator[(node, context)]
   Examples: node with depth, parent, grandparent, side, ancestor max.

5. Root-to-leaf path streams
   Tree -> Iterator[list[TreeNode]]
   Examples: path sum, path strings, leaf sequence, pseudo-palindromic paths.

6. Positional streams
   Tree -> Iterator[(node, row, col, heap_index)]
   Examples: vertical order, vertical traversal, maximum width, print tree.

7. Slot streams
   Tree -> Iterator[Optional[TreeNode]]
   Examples: completeness checks, null-gap reasoning.

8. BST ordered streams
   BST -> Iterator[TreeNode] in sorted order
   Examples: validate BST, kth smallest, min diff, two-sum, merge two BSTs.

Core mental model
-----------------
Do not ask only: "DFS or BFS?"
Ask: "What stream does this problem want the tree to expose?"

Examples:

- Traversal values wanted?                Use node/value stream.
- Per-level answer wanted?                Use level stream.
- Depth/parent/ancestor needed?           Use annotated stream.
- Root-to-leaf condition wanted?          Use path stream.
- Vertical/width/layout wanted?           Use positional stream.
- Missing children matter?                Use slot stream.
- BST sorted order wanted?                Use inorder ordered stream.
- Parent needs child summaries?           Stop using pure iteration; use bottom-up DP.

Coverage tally from attached 180-problem Binary Tree index
----------------------------------------------------------
Conservative tally: 67 / 180 problems are directly addressable where one of these
iteration primitives is the main reduction, sometimes with a small consumer or small
local mutation.

This does not mean the other 113 are unrelated to traversal. Almost every tree problem
traverses something. The distinction is whether iteration is the main solution shape
or only a subroutine inside construction, serialization, mutation, graph conversion,
or bottom-up tree DP.

The 67 directly addressable problem IDs are listed in ITERATION_MAIN_REDUCTION_PROBLEMS.
The solved examples in this module are listed in SOLVED_IN_THIS_FILE.
"""

from __future__ import annotations

from collections import Counter, defaultdict, deque
from dataclasses import dataclass
from heapq import nlargest
from math import inf
from typing import Deque, Iterable, Iterator, Optional, Sequence


# =============================================================================
# 0. Coverage constants from the attached 180-problem Binary Tree source index
# =============================================================================

TOTAL_PROBLEMS_IN_ATTACHED_INDEX = 180

ITERATION_MAIN_REDUCTION_PROBLEMS: set[int] = {
    # Plain DFS/value traversal streams.
    94, 144, 145, 2764,

    # Level streams and level-local consumers/mutations.
    102, 103, 107, 116, 117, 199, 513, 515, 637, 993,
    1161, 1302, 1602, 1609, 2415, 2471, 2583, 2641, 3157, 3831, 3902,

    # Depth/parent/ancestor annotated scans.
    104, 111, 671, 965, 1315, 1448, 1469,

    # Root-to-leaf / leaf-sequence / path-state streams.
    112, 113, 129, 257, 404, 872, 988, 1022, 1430, 1457,

    # Positional, geometric, slot, and completeness streams.
    222, 314, 655, 662, 919, 958, 987,

    # BST ordered streams.
    98, 99, 173, 230, 270, 272, 285, 501, 530, 538,
    653, 783, 897, 938, 1214, 1305, 1586, 2476,
}

SOLVED_IN_THIS_FILE: set[int] = {
    94, 98, 102, 103, 104, 107, 111, 112, 113, 129, 144, 145,
    173, 199, 222, 230, 257, 270, 272, 314, 404, 501, 513,
    515, 530, 637, 653, 655, 662, 783, 872, 938, 958, 965,
    987, 993, 1022, 1161, 1302, 1305, 1315, 1430, 1448, 1457,
    1469, 1586, 1602, 1609, 2415, 2471, 2583, 2641, 3157,
}


# =============================================================================
# 1. Representation and construction helpers
# =============================================================================

class TreeNode:
    def __init__(
        self,
        val: int = 0,
        left: Optional[TreeNode] = None,
        right: Optional[TreeNode] = None,
    ):
        self.val = val
        self.left = left
        self.right = right


class Node:
    """
    LeetCode-style node with next pointer.

    Used for 116 / 117 style problems if you want to practice next-right linking.
    The main iteration idea is still level streaming.
    """

    def __init__(
        self,
        val: int = 0,
        left: Optional[Node] = None,
        right: Optional[Node] = None,
        next: Optional[Node] = None,
    ):
        self.val = val
        self.left = left
        self.right = right
        self.next = next


def build_tree_level(values: Sequence[Optional[int]]) -> Optional[TreeNode]:
    """
    Testing helper: build a binary tree from LeetCode-style level-order values.

    Example:
        root = build_tree_level([1, 2, 3, None, 4])

    This is for practice/tests, not a core interview primitive.
    """
    if not values:
        return None

    first = values[0]
    if first is None:
        return None

    root = TreeNode(first)
    q: Deque[TreeNode] = deque([root])
    i = 1

    while q and i < len(values):
        node = q.popleft()

        if i < len(values) and values[i] is not None:
            node.left = TreeNode(values[i])
            q.append(node.left)
        i += 1

        if i < len(values) and values[i] is not None:
            node.right = TreeNode(values[i])
            q.append(node.right)
        i += 1

    return root


def is_leaf(node: Optional[TreeNode]) -> bool:
    """
    Leaf means real node with no children.
    None is not a leaf.
    """
    return node is not None and node.left is None and node.right is None


def children(node: TreeNode) -> Iterator[TreeNode]:
    """
    Real-node-only primitive.

    Contract:
        Caller is responsible for passing a real TreeNode, not None.

    Output:
        If node is a leaf, this yields no values. It behaves like an empty iterator.
    """
    if node.left is not None:
        yield node.left

    if node.right is not None:
        yield node.right


# =============================================================================
# 2. Primitive family A: node streams and value streams
# =============================================================================

# Why useful:
# A node stream turns a tree into a sequence. Once you have a sequence, consumers
# can map, filter, search, collect, count, and aggregate.
#
# Core tradeoff:
# Return Iterator[...] for reusable primitives.
# Return list[...] at LeetCode answer boundaries when the problem expects a list.


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
# bool means:
# False -> expand this node
# True  -> emit this node

def preorder_iter(root: Optional[TreeNode]) -> Iterator[TreeNode]:
    stack: list[Frame] = [(root, False)]

    while stack:
        node, emit = stack.pop()

        if node is None:
            continue

        if emit:
            yield node
            continue

        # desired order:
        # node, left, right
        #
        # stack is LIFO, so push reverse order:
        stack.append((node.right, False))
        stack.append((node.left, False))
        stack.append((node, True))


def inorder_iter(root: Optional[TreeNode]) -> Iterator[TreeNode]:
    stack: list[Frame] = [(root, False)]

    while stack:
        node, emit = stack.pop()

        if node is None:
            continue

        if emit:
            yield node
            continue

        # desired order:
        # left, node, right
        #
        # stack is LIFO, so push reverse order:
        stack.append((node.right, False))
        stack.append((node, True))
        stack.append((node.left, False))


def postorder_iter(root: Optional[TreeNode]) -> Iterator[TreeNode]:
    stack: list[Frame] = [(root, False)]

    while stack:
        node, emit = stack.pop()

        if node is None:
            continue

        if emit:
            yield node
            continue

        # desired order:
        # left, right, node
        #
        # stack is LIFO, so push reverse order:
        stack.append((node, True))
        stack.append((node.right, False))
        stack.append((node.left, False))


def values(nodes: Iterable[TreeNode]) -> Iterator[int]:
    return (node.val for node in nodes)


def preorder_values_iter(root: Optional[TreeNode]) -> Iterator[int]:
    return values(preorder_nodes(root))


def inorder_values_iter(root: Optional[TreeNode]) -> Iterator[int]:
    return values(inorder_nodes(root))


def postorder_values_iter(root: Optional[TreeNode]) -> Iterator[int]:
    return values(postorder_nodes(root))


# Complete solution examples from node/value streams.


def lc_094_inorder_traversal(root: Optional[TreeNode]) -> list[int]:
    return list(inorder_values_iter(root))


def lc_144_preorder_traversal(root: Optional[TreeNode]) -> list[int]:
    return list(preorder_values_iter(root))


def lc_145_postorder_traversal(root: Optional[TreeNode]) -> list[int]:
    return list(postorder_values_iter(root))


def lc_965_univalued_binary_tree(root: Optional[TreeNode]) -> bool:
    """
    965. Univalued Binary Tree

    Composition:
        node stream -> value stream -> all values equal first value
    """
    if root is None:
        return True

    first = root.val
    return all(node.val == first for node in preorder_nodes(root))


# =============================================================================
# 3. Primitive family B: level streams
# =============================================================================

# Why useful:
# A level stream turns a tree into rows. It is the main reduction for level order,
# zigzag, right side view, averages, largest values, cousins, level sums, and many
# level-local mutation problems.
#
# Invariant:
# At the start of each outer loop, the queue contains exactly the current level.
# The snapshot level_size = len(q) prevents current and next level from mixing.


def level_nodes(root: Optional[TreeNode]) -> Iterator[list[TreeNode]]:
    if root is None:
        return

    q: Deque[TreeNode] = deque([root])

    while q:
        level_size = len(q)
        level: list[TreeNode] = []

        for _ in range(level_size):
            node = q.popleft()
            level.append(node)

            if node.left is not None:
                q.append(node.left)
            if node.right is not None:
                q.append(node.right)

        yield level


def level_values(root: Optional[TreeNode]) -> list[list[int]]:
    return [[node.val for node in level] for level in level_nodes(root)]


def level_nodes_with_depth(root: Optional[TreeNode]) -> Iterator[tuple[int, list[TreeNode]]]:
    for depth, level in enumerate(level_nodes(root), start=0):
        yield depth, level


# Complete solution examples from level streams.


def lc_102_level_order(root: Optional[TreeNode]) -> list[list[int]]:
    return level_values(root)


def lc_103_zigzag_level_order(root: Optional[TreeNode]) -> list[list[int]]:
    result = []

    for depth, level in level_nodes_with_depth(root):
        row = [node.val for node in level]
        if depth % 2 == 1:
            row.reverse()
        result.append(row)

    return result


def lc_107_level_order_bottom(root: Optional[TreeNode]) -> list[list[int]]:
    return level_values(root)[::-1]


def lc_199_right_side_view(root: Optional[TreeNode]) -> list[int]:
    return [level[-1].val for level in level_nodes(root)]


def lc_513_find_bottom_left_value(root: Optional[TreeNode]) -> int:
    if root is None:
        raise ValueError("root must be non-empty for LeetCode 513")

    answer = root.val

    for level in level_nodes(root):
        answer = level[0].val

    return answer


def lc_515_largest_values(root: Optional[TreeNode]) -> list[int]:
    return [max(node.val for node in level) for level in level_nodes(root)]


def lc_637_average_of_levels(root: Optional[TreeNode]) -> list[float]:
    return [
        sum(node.val for node in level) / len(level)
        for level in level_nodes(root)
    ]


def lc_1161_max_level_sum(root: Optional[TreeNode]) -> int:
    """
    1161. Maximum Level Sum of a Binary Tree

    LeetCode uses 1-based level numbers.
    """
    best_level = 1
    best_sum = -inf

    for zero_depth, level in level_nodes_with_depth(root):
        total = sum(node.val for node in level)
        if total > best_sum:
            best_sum = total
            best_level = zero_depth + 1

    return best_level


def lc_1302_deepest_leaves_sum(root: Optional[TreeNode]) -> int:
    total = 0

    for level in level_nodes(root):
        total = sum(node.val for node in level)

    return total


def lc_2583_kth_largest_level_sum(root: Optional[TreeNode], k: int) -> int:
    sums = [sum(node.val for node in level) for level in level_nodes(root)]

    if len(sums) < k:
        return -1

    return nlargest(k, sums)[-1]


def lc_3157_level_with_minimum_sum(root: Optional[TreeNode]) -> int:
    """
    3157. Find the Level of Tree with Minimum Sum

    Assumes the LeetCode convention of returning the smallest 1-based level with
    the minimum sum.
    """
    best_level = 1
    best_sum = inf

    for zero_depth, level in level_nodes_with_depth(root):
        total = sum(node.val for node in level)
        if total < best_sum:
            best_sum = total
            best_level = zero_depth + 1

    return best_level


def lc_993_is_cousins(root: Optional[TreeNode], x: int, y: int) -> bool:
    """
    993. Cousins in Binary Tree

    Composition:
        level stream -> scan each level for x and y with parents -> compare parents
    """
    if root is None:
        return False

    q: Deque[tuple[TreeNode, Optional[TreeNode]]] = deque([(root, None)])

    while q:
        level_size = len(q)
        found: dict[int, Optional[TreeNode]] = {}

        for _ in range(level_size):
            node, parent = q.popleft()

            if node.val == x or node.val == y:
                found[node.val] = parent

            if node.left is not None:
                q.append((node.left, node))
            if node.right is not None:
                q.append((node.right, node))

        if x in found or y in found:
            return x in found and y in found and found[x] is not found[y]

    return False


def lc_1602_find_nearest_right_node(
    root: Optional[TreeNode],
    u: TreeNode,
) -> Optional[TreeNode]:
    """
    1602. Find Nearest Right Node in Binary Tree

    Composition:
        level stream -> find u's index in its level -> return next node if present
    """
    for level in level_nodes(root):
        for i, node in enumerate(level):
            if node is u:
                return level[i + 1] if i + 1 < len(level) else None

    return None


def lc_1609_even_odd_tree(root: Optional[TreeNode]) -> bool:
    """
    1609. Even Odd Tree

    Even-indexed levels: values are odd and strictly increasing.
    Odd-indexed levels: values are even and strictly decreasing.
    """
    for depth, level in level_nodes_with_depth(root):
        vals = [node.val for node in level]

        if depth % 2 == 0:
            if any(v % 2 == 0 for v in vals):
                return False
            if any(a >= b for a, b in zip(vals, vals[1:])):
                return False
        else:
            if any(v % 2 == 1 for v in vals):
                return False
            if any(a <= b for a, b in zip(vals, vals[1:])):
                return False

    return True


def lc_2415_reverse_odd_levels(root: Optional[TreeNode]) -> Optional[TreeNode]:
    """
    2415. Reverse Odd Levels of Binary Tree

    Composition:
        level stream -> on odd levels, reverse values pairwise

    This mutates values, not structure.
    """
    for depth, level in level_nodes_with_depth(root):
        if depth % 2 == 1:
            vals = [node.val for node in level][::-1]
            for node, val in zip(level, vals):
                node.val = val

    return root


def _min_swaps_to_sort(nums: list[int]) -> int:
    pairs = sorted((value, index) for index, value in enumerate(nums))
    visited = [False] * len(nums)
    swaps = 0

    for i in range(len(nums)):
        if visited[i] or pairs[i][1] == i:
            continue

        cycle_len = 0
        j = i

        while not visited[j]:
            visited[j] = True
            j = pairs[j][1]
            cycle_len += 1

        swaps += cycle_len - 1

    return swaps


def lc_2471_minimum_operations_to_sort_by_level(root: Optional[TreeNode]) -> int:
    """
    2471. Minimum Number of Operations to Sort a Binary Tree by Level

    Composition:
        level stream -> values per level -> min swaps to sort each row
    """
    return sum(
        _min_swaps_to_sort([node.val for node in level])
        for level in level_nodes(root)
    )


def lc_2641_replace_value_in_tree(root: Optional[TreeNode]) -> Optional[TreeNode]:
    """
    2641. Cousins in Binary Tree II

    Composition:
        level stream -> next level total -> sibling group subtraction

    This is still level-iteration driven, even though it mutates node values.
    """
    if root is None:
        return None

    root.val = 0
    current = [root]

    while current:
        next_level = [child for node in current for child in children(node)]
        next_total = sum(node.val for node in next_level)

        for node in current:
            sibling_sum = 0
            if node.left is not None:
                sibling_sum += node.left.val
            if node.right is not None:
                sibling_sum += node.right.val

            if node.left is not None:
                node.left.val = next_total - sibling_sum
            if node.right is not None:
                node.right.val = next_total - sibling_sum

        current = next_level

    return root


# =============================================================================
# 4. Primitive family C: annotated streams
# =============================================================================

# Why useful:
# Sometimes a node alone is insufficient. The consumer needs depth, parent,
# grandparent, side, or ancestor state. Annotated streams keep traversal reusable
# while carrying just enough context.


@dataclass(frozen=True)
class NodeContext:
    node: TreeNode
    parent: Optional[TreeNode]
    grandparent: Optional[TreeNode]
    depth: int
    is_left_child: bool


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


def preorder_with_context(root: Optional[TreeNode]) -> Iterator[NodeContext]:
    def dfs(
        node: Optional[TreeNode],
        parent: Optional[TreeNode],
        grandparent: Optional[TreeNode],
        depth: int,
        is_left_child: bool,
    ) -> Iterator[NodeContext]:
        if node is None:
            return

        yield NodeContext(node, parent, grandparent, depth, is_left_child)
        yield from dfs(node.left, node, parent, depth + 1, True)
        yield from dfs(node.right, node, parent, depth + 1, False)

    yield from dfs(root, None, None, 0, False)


# Complete solution examples from annotated streams.


def lc_104_max_depth(root: Optional[TreeNode]) -> int:
    if root is None:
        return 0

    return max(depth for _, depth in preorder_with_depth(root)) + 1


def lc_111_min_depth(root: Optional[TreeNode]) -> int:
    """
    111. Minimum Depth of Binary Tree

    BFS level stream gives the first real leaf at the shallowest level.
    """
    for depth, level in level_nodes_with_depth(root):
        if any(is_leaf(node) for node in level):
            return depth + 1

    return 0


def lc_1315_sum_even_grandparent(root: Optional[TreeNode]) -> int:
    return sum(
        context.node.val
        for context in preorder_with_context(root)
        if context.grandparent is not None and context.grandparent.val % 2 == 0
    )


def lc_1469_get_lonely_nodes(root: Optional[TreeNode]) -> list[int]:
    result = []

    for context in preorder_with_context(root):
        parent = context.parent
        if parent is None:
            continue

        is_lonely_left = context.is_left_child and parent.right is None
        is_lonely_right = not context.is_left_child and parent.left is None

        if is_lonely_left or is_lonely_right:
            result.append(context.node.val)

    return result


def lc_1448_good_nodes(root: Optional[TreeNode]) -> int:
    """
    1448. Count Good Nodes in Binary Tree

    This one needs ancestor max, so it is slightly more than a plain node stream.
    It is still top-down annotated iteration: carry max_so_far downward.
    """
    def dfs(node: Optional[TreeNode], max_so_far: int) -> Iterator[TreeNode]:
        if node is None:
            return

        if node.val >= max_so_far:
            yield node

        new_max = max(max_so_far, node.val)
        yield from dfs(node.left, new_max)
        yield from dfs(node.right, new_max)

    return sum(1 for _ in dfs(root, -inf))


# =============================================================================
# 5. Primitive family D: root-to-leaf path streams
# =============================================================================

# Why useful:
# Many problems are not asking about arbitrary nodes. They ask about complete
# root-to-leaf paths. Emit only complete paths, then compose consumers.
#
# Invariant:
# path contains exactly root -> current node during the recursive frame.
# path.pop() restores caller-visible state before returning.


def root_to_leaf_paths(root: Optional[TreeNode]) -> Iterator[list[TreeNode]]:
    path: list[TreeNode] = []

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


def root_to_leaf_value_paths(root: Optional[TreeNode]) -> Iterator[list[int]]:
    return ([node.val for node in path] for path in root_to_leaf_paths(root))


def leaf_nodes(root: Optional[TreeNode]) -> Iterator[TreeNode]:
    return (path[-1] for path in root_to_leaf_paths(root))


# Complete solution examples from root-to-leaf path streams.


def lc_112_has_path_sum(root: Optional[TreeNode], target_sum: int) -> bool:
    return any(sum(path) == target_sum for path in root_to_leaf_value_paths(root))


def lc_113_path_sum_ii(root: Optional[TreeNode], target_sum: int) -> list[list[int]]:
    return [
        path
        for path in root_to_leaf_value_paths(root)
        if sum(path) == target_sum
    ]


def lc_129_sum_numbers(root: Optional[TreeNode]) -> int:
    return sum(
        int("".join(str(v) for v in path))
        for path in root_to_leaf_value_paths(root)
    )


def lc_1022_sum_root_to_leaf_binary_numbers(root: Optional[TreeNode]) -> int:
    return sum(
        int("".join(str(v) for v in path), 2)
        for path in root_to_leaf_value_paths(root)
    )


def lc_257_binary_tree_paths(root: Optional[TreeNode]) -> list[str]:
    return [
        "->".join(str(v) for v in path)
        for path in root_to_leaf_value_paths(root)
    ]


def lc_872_leaf_similar(root1: Optional[TreeNode], root2: Optional[TreeNode]) -> bool:
    return [node.val for node in leaf_nodes(root1)] == [node.val for node in leaf_nodes(root2)]


def lc_1430_is_valid_sequence(root: Optional[TreeNode], arr: list[int]) -> bool:
    return any(path == arr for path in root_to_leaf_value_paths(root))


def lc_1457_pseudo_palindromic_paths(root: Optional[TreeNode]) -> int:
    """
    1457. Pseudo-Palindromic Paths in a Binary Tree

    A path can be permuted into a palindrome iff at most one value has odd count.
    """
    count = 0

    for path in root_to_leaf_value_paths(root):
        freq = Counter(path)
        odd_count = sum(v % 2 for v in freq.values())
        if odd_count <= 1:
            count += 1

    return count


def lc_404_sum_of_left_leaves(root: Optional[TreeNode]) -> int:
    """
    404. Sum of Left Leaves

    This is better as an annotated stream than a full path stream.
    """
    return sum(
        context.node.val
        for context in preorder_with_context(root)
        if context.is_left_child and is_leaf(context.node)
    )


# =============================================================================
# 6. Primitive family E: positional and geometric streams
# =============================================================================

# Why useful:
# Some tree problems are geometric. They care about row, column, virtual heap index,
# or missing gaps. A plain DFS/BFS node stream is too weak.


def bfs_with_position(
    root: Optional[TreeNode],
) -> Iterator[tuple[TreeNode, int, int, int]]:
    """
    Yields:
        node, row, col, heap_index

    row:
        root row = 0

    col:
        left child  = col - 1
        right child = col + 1

    heap_index:
        left child  = 2 * i
        right child = 2 * i + 1
    """
    if root is None:
        return

    q: Deque[tuple[TreeNode, int, int, int]] = deque([(root, 0, 0, 0)])

    while q:
        node, row, col, idx = q.popleft()
        yield node, row, col, idx

        if node.left is not None:
            q.append((node.left, row + 1, col - 1, 2 * idx))
        if node.right is not None:
            q.append((node.right, row + 1, col + 1, 2 * idx + 1))


def indexed_levels(root: Optional[TreeNode]) -> Iterator[list[tuple[TreeNode, int]]]:
    """
    Specialized positional stream for width.

    Normalizes indices level-by-level so they do not grow exponentially.
    """
    if root is None:
        return

    q: Deque[tuple[TreeNode, int]] = deque([(root, 0)])

    while q:
        level_size = len(q)
        base = q[0][1]
        level: list[tuple[TreeNode, int]] = []

        for _ in range(level_size):
            node, idx = q.popleft()
            idx -= base
            level.append((node, idx))

            if node.left is not None:
                q.append((node.left, 2 * idx))
            if node.right is not None:
                q.append((node.right, 2 * idx + 1))

        yield level


# Complete solution examples from positional streams.


def lc_314_vertical_order(root: Optional[TreeNode]) -> list[list[int]]:
    """
    314. Binary Tree Vertical Order Traversal

    BFS positional stream preserves top-to-bottom, left-to-right order within column.
    """
    columns: dict[int, list[int]] = defaultdict(list)

    for node, _, col, _ in bfs_with_position(root):
        columns[col].append(node.val)

    return [columns[col] for col in sorted(columns)]


def lc_987_vertical_traversal(root: Optional[TreeNode]) -> list[list[int]]:
    """
    987. Vertical Order Traversal of a Binary Tree

    Sort by column, then row, then value.
    """
    points = [
        (col, row, node.val)
        for node, row, col, _ in bfs_with_position(root)
    ]
    points.sort()

    result: list[list[int]] = []
    current_col: Optional[int] = None

    for col, _, val in points:
        if col != current_col:
            result.append([])
            current_col = col
        result[-1].append(val)

    return result


def lc_662_width_of_binary_tree(root: Optional[TreeNode]) -> int:
    best = 0

    for level in indexed_levels(root):
        best = max(best, level[-1][1] - level[0][1] + 1)

    return best


def lc_655_print_tree(root: Optional[TreeNode]) -> list[list[str]]:
    """
    655. Print Binary Tree

    This is a layout problem. We first need tree height, then place each node at
    a computed row/column.
    """
    height = lc_104_max_depth(root)
    if height == 0:
        return []

    rows = height
    cols = 2 ** height - 1
    grid = [["" for _ in range(cols)] for _ in range(rows)]

    def place(node: Optional[TreeNode], row: int, left: int, right: int) -> None:
        if node is None or row == rows:
            return

        mid = (left + right) // 2
        grid[row][mid] = str(node.val)
        place(node.left, row + 1, left, mid - 1)
        place(node.right, row + 1, mid + 1, right)

    place(root, 0, 0, cols - 1)
    return grid


# =============================================================================
# 7. Primitive family F: slot streams and completeness
# =============================================================================

# Why useful:
# Normal node streams hide missing children. Completeness problems need missing
# child slots as evidence. Therefore expose Optional[TreeNode], not only TreeNode.


def level_slots(root: Optional[TreeNode]) -> Iterator[Optional[TreeNode]]:
    q: Deque[Optional[TreeNode]] = deque([root])

    while q:
        node = q.popleft()
        yield node

        if node is not None:
            q.append(node.left)
            q.append(node.right)


def lc_958_is_complete_tree(root: Optional[TreeNode]) -> bool:
    """
    958. Check Completeness of a Binary Tree

    In level-order slot traversal, once a None slot appears, every later slot
    must also be None.
    """
    seen_null_slot = False

    for slot in level_slots(root):
        if slot is None:
            seen_null_slot = True
        elif seen_null_slot:
            return False

    return True


def lc_222_count_nodes_bfs(root: Optional[TreeNode]) -> int:
    """
    222. Count Complete Tree Nodes

    This BFS version is correct but not the optimal O(log^2 n) complete-tree trick.
    It is included to show that iteration can address it, but not optimally.
    """
    return sum(1 for node in preorder_nodes(root))


# =============================================================================
# 8. Primitive family G: BST ordered streams
# =============================================================================

# Why useful:
# In a BST, inorder traversal exposes values in sorted order. That one fact turns
# tree problems into sorted-stream problems: validate, kth, min-diff, merge,
# mode, two-sum, closest values, and iterators.


def bst_values(root: Optional[TreeNode]) -> Iterator[int]:
    return inorder_values_iter(root)


def lc_098_is_valid_bst(root: Optional[TreeNode]) -> bool:
    prev = -inf

    for value in bst_values(root):
        if value <= prev:
            return False
        prev = value

    return True


def lc_230_kth_smallest(root: Optional[TreeNode], k: int) -> int:
    for i, value in enumerate(bst_values(root), start=1):
        if i == k:
            return value

    raise ValueError("k is larger than the number of nodes")


def lc_530_minimum_absolute_difference(root: Optional[TreeNode]) -> int:
    prev: Optional[int] = None
    best = inf

    for value in bst_values(root):
        if prev is not None:
            best = min(best, value - prev)
        prev = value

    return int(best)


def lc_783_min_diff_in_bst(root: Optional[TreeNode]) -> int:
    return lc_530_minimum_absolute_difference(root)


def lc_501_find_mode(root: Optional[TreeNode]) -> list[int]:
    """
    501. Find Mode in Binary Search Tree

    Inorder makes equal values consecutive.
    """
    modes: list[int] = []
    prev: Optional[int] = None
    curr_count = 0
    best_count = 0

    for value in bst_values(root):
        if value == prev:
            curr_count += 1
        else:
            prev = value
            curr_count = 1

        if curr_count > best_count:
            best_count = curr_count
            modes = [value]
        elif curr_count == best_count:
            modes.append(value)

    return modes


def lc_653_find_target(root: Optional[TreeNode], k: int) -> bool:
    seen: set[int] = set()

    for value in bst_values(root):
        if k - value in seen:
            return True
        seen.add(value)

    return False


def lc_938_range_sum_bst(root: Optional[TreeNode], low: int, high: int) -> int:
    """
    938. Range Sum of BST

    This stream version is simple. A more optimized BST version prunes branches.
    """
    total = 0

    for value in bst_values(root):
        if value > high:
            break
        if value >= low:
            total += value

    return total


def lc_1305_get_all_elements(
    root1: Optional[TreeNode],
    root2: Optional[TreeNode],
) -> list[int]:
    """
    1305. All Elements in Two Binary Search Trees

    Composition:
        inorder stream from BST 1 + inorder stream from BST 2 -> merge sorted streams
    """
    a = list(bst_values(root1))
    b = list(bst_values(root2))
    i = j = 0
    result: list[int] = []

    while i < len(a) and j < len(b):
        if a[i] <= b[j]:
            result.append(a[i])
            i += 1
        else:
            result.append(b[j])
            j += 1

    result.extend(a[i:])
    result.extend(b[j:])
    return result


def lc_270_closest_value(root: Optional[TreeNode], target: float) -> int:
    """
    270. Closest Binary Search Tree Value

    This stream version is simple. A BST-guided search can do better on balanced trees.
    """
    if root is None:
        raise ValueError("root must be non-empty")

    return min(bst_values(root), key=lambda value: (abs(value - target), value))


def lc_272_closest_k_values(
    root: Optional[TreeNode],
    target: float,
    k: int,
) -> list[int]:
    return sorted(
        bst_values(root),
        key=lambda value: abs(value - target),
    )[:k]


class BSTIterator:
    """
    173. Binary Search Tree Iterator

    This is an external iterator around iterative inorder traversal.
    """

    def __init__(self, root: Optional[TreeNode]):
        self.stack: list[TreeNode] = []
        self._push_left(root)

    def _push_left(self, node: Optional[TreeNode]) -> None:
        while node is not None:
            self.stack.append(node)
            node = node.left

    def next(self) -> int:
        node = self.stack.pop()
        self._push_left(node.right)
        return node.val

    def hasNext(self) -> bool:
        return bool(self.stack)


class BSTIteratorII:
    """
    1586. Binary Search Tree Iterator II

    The forward iterator is still iterative inorder. The extra list caches history
    so prev() can move backward.
    """

    def __init__(self, root: Optional[TreeNode]):
        self.stack: list[TreeNode] = []
        self.values: list[int] = []
        self.index = -1
        self._push_left(root)

    def _push_left(self, node: Optional[TreeNode]) -> None:
        while node is not None:
            self.stack.append(node)
            node = node.left

    def hasNext(self) -> bool:
        return self.index + 1 < len(self.values) or bool(self.stack)

    def next(self) -> int:
        self.index += 1

        if self.index == len(self.values):
            node = self.stack.pop()
            self.values.append(node.val)
            self._push_left(node.right)

        return self.values[self.index]

    def hasPrev(self) -> bool:
        return self.index > 0

    def prev(self) -> int:
        self.index -= 1
        return self.values[self.index]


# =============================================================================
# 9. Composition summary as practice notes
# =============================================================================

"""
Composition chains to drill
---------------------------

A. Plain traversal

    preorder_nodes / inorder_nodes / postorder_nodes
    -> values(...)
    -> list(...)
    -> 94, 144, 145

B. Level traversal

    level_nodes
    -> per-level value row
    -> level order / zigzag / bottom-up
    -> 102, 103, 107

    level_nodes
    -> take first/last node per level
    -> bottom-left / right-side view
    -> 513, 199

    level_nodes
    -> aggregate each row
    -> largest / average / max sum / deepest leaves sum / kth largest level sum
    -> 515, 637, 1161, 1302, 2583

    level_nodes
    -> compare nodes within same level
    -> cousins / nearest right / even-odd tree
    -> 993, 1602, 1609

    level_nodes
    -> mutate values level-wise
    -> reverse odd levels / cousin replacement
    -> 2415, 2641

C. Annotated traversal

    preorder_with_context
    -> parent/grandparent/side-aware filters
    -> left leaves / even grandparent / lonely nodes
    -> 404, 1315, 1469

    top-down annotated DFS
    -> carry ancestor max
    -> count good nodes
    -> 1448

D. Root-to-leaf path stream

    root_to_leaf_paths
    -> value paths
    -> sum / string / equality / frequency check
    -> 112, 113, 129, 257, 1022, 1430, 1457

    root_to_leaf_paths
    -> last node of each path
    -> leaf sequence
    -> 872

E. Positional stream

    bfs_with_position
    -> group by column
    -> vertical order
    -> 314

    bfs_with_position
    -> sort by column, row, value
    -> vertical traversal
    -> 987

    indexed_levels
    -> rightmost_index - leftmost_index + 1
    -> maximum width
    -> 662

F. Slot stream

    level_slots
    -> after first None, no real node may appear
    -> completeness
    -> 958

G. BST ordered stream

    inorder_nodes on BST
    -> sorted value stream
    -> validate / kth / min diff / mode / two-sum / merge BSTs
    -> 98, 230, 530, 501, 653, 1305

Interview instinct
------------------

If the problem can be reduced to a stream, use an iteration primitive.
If the parent needs a synthesized answer from children, use bottom-up recursion/DP.
If the tree must be modified structurally, traversal may still guide you, but mutation
safety becomes the main concern.
"""


# =============================================================================
# 10. Tiny smoke test helpers
# =============================================================================


def _demo_tree() -> Optional[TreeNode]:
    return build_tree_level([1, 2, 3, 4, 5, None, 7])


def _run_smoke_tests() -> None:
    root = _demo_tree()

    assert lc_144_preorder_traversal(root) == [1, 2, 4, 5, 3, 7]
    assert lc_094_inorder_traversal(root) == [4, 2, 5, 1, 3, 7]
    assert lc_145_postorder_traversal(root) == [4, 5, 2, 7, 3, 1]
    assert lc_102_level_order(root) == [[1], [2, 3], [4, 5, 7]]
    assert lc_103_zigzag_level_order(root) == [[1], [3, 2], [4, 5, 7]]
    assert lc_199_right_side_view(root) == [1, 3, 7]
    assert lc_513_find_bottom_left_value(root) == 4
    assert lc_104_max_depth(root) == 3
    assert lc_111_min_depth(root) == 3
    assert lc_662_width_of_binary_tree(root) == 4
    assert lc_958_is_complete_tree(root) is False


if __name__ == "__main__":
    _run_smoke_tests()
    print("smoke tests passed")
