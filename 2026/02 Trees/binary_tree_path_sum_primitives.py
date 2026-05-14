"""
Binary Tree Path Sum Primitives

This file captures the reusable primitives for the Path Sum family.

Problem families covered:

1. 112. Path Sum
   - Root-to-leaf existence
   - Primitive: leaf-aware remaining-sum DFS

2. 113. Path Sum II
   - Root-to-leaf path enumeration
   - Primitive: mutable path + backtracking + leaf check

3. 129. Sum Root to Leaf Numbers
   - Root-to-leaf numeric accumulation
   - Primitive: downward accumulator DFS

4. 437. Path Sum III
   - Any downward path, not necessarily starting at root or ending at leaf
   - Primitive: prefix-sum counter on current root path

5. 124. Binary Tree Maximum Path Sum
   - Any path through the tree
   - Primitive: postorder one-sided gain + global split answer

Core distinctions:

112 / 113:
    path must start at root
    path must end at leaf

437:
    path can start at any ancestor
    path can end at current node
    path must go downward

124:
    path can start and end anywhere
    path may pass through a node by joining left + node + right
    but the value returned to a parent must be one-sided
"""

from collections import defaultdict
from typing import DefaultDict, List, Optional


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
    """
    A leaf is a real node with no children.

    Important:
        None is not a leaf.

    This prevents the classic wrong base case in root-to-leaf problems.
    """

    return node is not None and node.left is None and node.right is None


# ---------------------------------------------------------------------
# Primitive 1:
# Leaf-aware remaining-sum DFS
#
# Solves:
#   112. Path Sum
#
# Mental model:
#   remaining means:
#       how much more this root-to-current path still needs.
#
#   At a leaf:
#       success iff remaining - leaf.val == 0.
# ---------------------------------------------------------------------


def has_root_to_leaf_sum(root: Optional[TreeNode], target: int) -> bool:
    def dfs(node: Optional[TreeNode], remaining: int) -> bool:
        if node is None:
            return False

        remaining -= node.val

        if is_leaf(node):
            return remaining == 0

        return dfs(node.left, remaining) or dfs(node.right, remaining)

    return dfs(root, target)


class PathSumSolution:
    """
    LeetCode 112. Path Sum
    """

    def hasPathSum(self, root: Optional[TreeNode], targetSum: int) -> bool:
        return has_root_to_leaf_sum(root, targetSum)


# ---------------------------------------------------------------------
# Primitive 2:
# Backtracking root-to-leaf path collector
#
# Solves:
#   113. Path Sum II
#
# Mental model:
#   path always equals the exact root-to-current path.
#   After dfs(node) returns, path must be restored.
# ---------------------------------------------------------------------


def root_to_leaf_paths_with_sum(
    root: Optional[TreeNode],
    target: int,
) -> List[List[int]]:
    ans: List[List[int]] = []
    path: List[int] = []

    def dfs(node: Optional[TreeNode], remaining: int) -> None:
        if node is None:
            return

        path.append(node.val)
        remaining -= node.val

        if is_leaf(node) and remaining == 0:
            ans.append(path.copy())
        else:
            dfs(node.left, remaining)
            dfs(node.right, remaining)

        path.pop()

    dfs(root, target)
    return ans


class PathSumIISolution:
    """
    LeetCode 113. Path Sum II
    """

    def pathSum(self, root: Optional[TreeNode], targetSum: int) -> List[List[int]]:
        return root_to_leaf_paths_with_sum(root, targetSum)


# ---------------------------------------------------------------------
# Primitive 3:
# Generic downward accumulator DFS
#
# Solves:
#   129. Sum Root to Leaf Numbers
#   1022. Sum of Root To Leaf Binary Numbers
#
# Mental model:
#   state flows parent -> child.
#
# For 129:
#   number_so_far = old_number * 10 + node.val
# ---------------------------------------------------------------------


def sum_root_to_leaf_numbers(root: Optional[TreeNode]) -> int:
    def dfs(node: Optional[TreeNode], value: int) -> int:
        if node is None:
            return 0

        value = value * 10 + node.val

        if is_leaf(node):
            return value

        return dfs(node.left, value) + dfs(node.right, value)

    return dfs(root, 0)


class SumRootToLeafNumbersSolution:
    """
    LeetCode 129. Sum Root to Leaf Numbers
    """

    def sumNumbers(self, root: Optional[TreeNode]) -> int:
        return sum_root_to_leaf_numbers(root)


def sum_root_to_leaf_binary_numbers(root: Optional[TreeNode]) -> int:
    """
    LeetCode 1022. Sum of Root To Leaf Binary Numbers

    Same primitive as 129, but base is 2 instead of 10.
    """

    def dfs(node: Optional[TreeNode], value: int) -> int:
        if node is None:
            return 0

        value = value * 2 + node.val

        if is_leaf(node):
            return value

        return dfs(node.left, value) + dfs(node.right, value)

    return dfs(root, 0)


class SumRootToLeafBinaryNumbersSolution:
    """
    LeetCode 1022. Sum of Root To Leaf Binary Numbers
    """

    def sumRootToLeaf(self, root: Optional[TreeNode]) -> int:
        return sum_root_to_leaf_binary_numbers(root)


# ---------------------------------------------------------------------
# Primitive 4:
# Prefix-sum counter on current root path
#
# Solves:
#   437. Path Sum III
#
# Why this is different from 112 / 113:
#   Paths do not have to start at root.
#   Paths do not have to end at leaf.
#   They only need to go downward.
#
# Mental model:
#   prefix_count contains prefix sums only for the current root-to-parent path.
#
#   When visiting node:
#       current_sum = root-to-current sum
#
#   A downward path ending at current node has sum target iff:
#       ancestor_prefix = current_sum - target
#
# The decrement during backtracking is essential:
#   prefix_count[curr_sum] -= 1
#
# Without it, prefix sums from the left subtree leak into the right subtree.
# ---------------------------------------------------------------------


def count_downward_paths_with_sum(root: Optional[TreeNode], target: int) -> int:
    count = 0
    prefix_count: DefaultDict[int, int] = defaultdict(int)
    prefix_count[0] = 1

    def dfs(node: Optional[TreeNode], curr_sum: int) -> None:
        nonlocal count

        if node is None:
            return

        curr_sum += node.val

        count += prefix_count[curr_sum - target]

        prefix_count[curr_sum] += 1
        dfs(node.left, curr_sum)
        dfs(node.right, curr_sum)
        prefix_count[curr_sum] -= 1

    dfs(root, 0)
    return count


class PathSumIIISolution:
    """
    LeetCode 437. Path Sum III
    """

    def pathSum(self, root: Optional[TreeNode], targetSum: int) -> int:
        return count_downward_paths_with_sum(root, targetSum)


# ---------------------------------------------------------------------
# Primitive 5:
# Postorder one-sided gain + global split answer
#
# Solves:
#   124. Binary Tree Maximum Path Sum
#
# This is tree DP, not merely downward DFS.
#
# Crucial distinction:
#
#   global candidate at node:
#       left_gain + node.val + right_gain
#
#   value returned to parent:
#       node.val + max(left_gain, right_gain)
#
# Why?
#   A path passed upward to the parent must remain a single chain.
#   It cannot take both left and right branches and then also connect
#   to the parent.
# ---------------------------------------------------------------------


def max_path_sum(root: Optional[TreeNode]) -> int:
    best = float("-inf")

    def gain(node: Optional[TreeNode]) -> int:
        nonlocal best

        if node is None:
            return 0

        left = max(0, gain(node.left))
        right = max(0, gain(node.right))

        best = max(best, node.val + left + right)

        return node.val + max(left, right)

    gain(root)
    return int(best)


class BinaryTreeMaximumPathSumSolution:
    """
    LeetCode 124. Binary Tree Maximum Path Sum
    """

    def maxPathSum(self, root: Optional[TreeNode]) -> int:
        return max_path_sum(root)


# ---------------------------------------------------------------------
# Optional helper:
# Build a binary tree from LeetCode-style level-order values.
#
# This is only for local testing. LeetCode normally provides TreeNode.
# ---------------------------------------------------------------------


def build_tree(values: List[Optional[int]]) -> Optional[TreeNode]:
    if not values:
        return None

    nodes = [
        TreeNode(value) if value is not None else None
        for value in values
    ]

    child = 1

    for node in nodes:
        if node is None:
            continue

        if child < len(nodes):
            node.left = nodes[child]
            child += 1

        if child < len(nodes):
            node.right = nodes[child]
            child += 1

    return nodes[0]


# ---------------------------------------------------------------------
# Suggested drill order:
#
# 1. 112 Path Sum
#    primitive:
#       leaf-aware remaining-sum DFS
#
# 2. 113 Path Sum II
#    primitive:
#       mutable path + backtracking + leaf check
#
# 3. 129 Sum Root to Leaf Numbers
#    primitive:
#       downward accumulator
#
# 4. 437 Path Sum III
#    primitive:
#       prefix-sum counter on current root path
#
# 5. 124 Binary Tree Maximum Path Sum
#    primitive:
#       postorder one-sided gain + global split answer
#
# 6. 666 Path Sum IV, if needed
#    primitive:
#       encoded-position tree + root-to-leaf accumulator
# ---------------------------------------------------------------------
