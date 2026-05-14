"""

111. Minimum Depth of Binary Tree
Easy

Given a binary tree, find its minimum depth.

The minimum depth is the number of nodes along the shortest path from the root node down to the nearest leaf node.

Note: A leaf is a node with no children.



Example 1:


Input: root = [3,9,20,null,null,15,7]
Output: 2
Example 2:

Input: root = [2,null,3,null,4,null,5,null,6]
Output: 5


Constraints:

The number of nodes in the tree is in the range [0, 105].
-1000 <= Node.val <= 1000

Seen this question in a real interview before?
1/6
Yes
No
Accepted
1,676,973/3.2M
Acceptance Rate
52.8%

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

def min_depth(node: Optional[TreeNode]) -> int:
    if node is None:
        return 0

    if is_leaf(node):
        return 1

    if node.left is None:
        return 1 + min_depth(node.right)

    if node.right is None:
        return 1 + min_depth(node.left)

    return 1 + min(min_depth(node.left), min_depth(node.right))


class Solution:
    def minDepth(self, root: Optional[TreeNode]) -> int:
        return min_depth(root)
