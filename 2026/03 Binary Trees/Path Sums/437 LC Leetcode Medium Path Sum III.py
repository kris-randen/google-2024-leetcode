"""


437. Path Sum III
Medium

Given the root of a binary tree and an integer targetSum, return the number of paths where the sum of the values along the path equals targetSum.

The path does not need to start or end at the root or a leaf, but it must go downwards (i.e., traveling only from parent nodes to child nodes).

Example 1:

Input: root = [10,5,-3,3,2,null,11,3,-2,null,1], targetSum = 8
Output: 3
Explanation: The paths that sum to 8 are shown.
Example 2:

Input: root = [5,4,8,11,null,13,4,7,2,null,null,5,1], targetSum = 22
Output: 3

"""

from typing import Optional

# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def is_leaf(node: Optional[TreeNode]) -> bool:
    return node is not None and node.left is None and node.right is None

def paths_with_sum(root: Optional[TreeNode], target: int):
    def dfs(node: Optional[TreeNode], remaining: int) -> int:
        if node is None:
            return 0

        remaining -= (val := node.val)

        found_here = 1 if remaining == 0 else 0

        l_paths, r_paths = dfs(node.left, remaining), dfs(node.right, remaining)

        return found_here + l_paths + r_paths

    def paths_all(node: Optional[TreeNode], target) -> int:
        if node is None: return 0
        return dfs(node, target) + paths_all(node.left, target) + paths_all(node.right, target)

    return paths_all(root, target)


class Solution:
    def pathSum(self, root: Optional[TreeNode], targetSum: int) -> int:
        return paths_with_sum(root, targetSum)


