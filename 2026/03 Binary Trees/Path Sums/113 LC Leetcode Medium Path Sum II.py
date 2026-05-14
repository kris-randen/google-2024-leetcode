"""

113. Path Sum II
Solved
Medium

Given the root of a binary tree and an integer targetSum, return all root-to-leaf paths where the sum of the node values in the path equals targetSum. Each path should be returned as a list of the node values, not node references.

A root-to-leaf path is a path starting from the root and ending at any leaf node. A leaf is a node with no children.



Example 1:


Input: root = [5,4,8,11,null,13,4,7,2,null,null,5,1], targetSum = 22
Output: [[5,4,11,2],[5,8,4,5]]
Explanation: There are two paths whose sum equals targetSum:
5 + 4 + 11 + 2 = 22
5 + 8 + 4 + 5 = 22
Example 2:


Input: root = [1,2,3], targetSum = 5
Output: []
Example 3:

Input: root = [1,2], targetSum = 0
Output: []


Constraints:

The number of nodes in the tree is in the range [0, 5000].
-1000 <= Node.val <= 1000
-1000 <= targetSum <= 1000

Seen this question in a real interview before?
1/6
Yes
No
Accepted
1,175,324/1.9M
Acceptance Rate
62.1%

"""
from typing import List, Optional


# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
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

def path_sums(root: Optional[TreeNode], target: int) -> List[List[int]]:
    def dfs(node: Optional[TreeNode], remaining: int) -> List[List[int]]:
        if node is None:
            return []

        remaining -= (val := node.val)

        if is_leaf(node):
            return [[node.val]] if remaining == 0 else []

        l_paths, r_paths = \
        (
            dfs(node.left, remaining),
            dfs(node.right, remaining)
        )

        [path.append(val) for path in l_paths]
        [path.append(val) for path in r_paths]

        return l_paths + r_paths

    return [list(reversed(path)) for path in dfs(root, target)]

class Solution:
    def pathSum(self, root: Optional[TreeNode], targetSum: int) -> List[List[int]]:
        return path_sums(root, targetSum)
