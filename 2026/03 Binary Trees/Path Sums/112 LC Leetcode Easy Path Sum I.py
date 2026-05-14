"""

112. Path Sum
Easy

Given the root of a binary tree and an integer targetSum, return true if the tree has a root-to-leaf path such that adding up all the values along the path equals targetSum.

A leaf is a node with no children.



Example 1:


Input: root = [5,4,8,11,null,13,4,7,2,null,null,null,1], targetSum = 22
Output: true
Explanation: The root-to-leaf path with the target sum is shown.
Example 2:


Input: root = [1,2,3], targetSum = 5
Output: false
Explanation: There are two root-to-leaf paths in the tree:
(1 --> 2): The sum is 3.
(1 --> 3): The sum is 4.
There is no root-to-leaf path with sum = 5.
Example 3:

Input: root = [], targetSum = 0
Output: false
Explanation: Since the tree is empty, there are no root-to-leaf paths.


Constraints:

The number of nodes in the tree is in the range [0, 5000].
-1000 <= Node.val <= 1000
-1000 <= targetSum <= 1000

Seen this question in a real interview before?
1/6
Yes
No
Accepted
2,143,165/3.9M
Acceptance Rate
54.9%

"""
from mimetypes import read_mime_types
from typing import Optional


# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def is_leaf(node: Optional[TreeNode]):
    return \
    (
        node is not None and
        node.left is None and
        node.right is None
    )

def path_sum(root: Optional[TreeNode], target) -> bool:
    def dfs(node: Optional[TreeNode], remaining: int) -> bool:
        if node is None:
            return False

        remaining -= node.val

        if is_leaf(node):
            return remaining == 0

        return \
        (
            dfs(node.left, remaining) or
            dfs(node.right, remaining)
        )

    return dfs(root, target)

class Solution:
    def hasPathSum(self, root: Optional[TreeNode], targetSum: int) -> bool:
        return path_sum(root, targetSum)
