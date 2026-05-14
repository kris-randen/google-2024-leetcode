"""

226. Invert Binary Tree
Solved
Easy

Given the root of a binary tree, invert the tree, and return its root.



Example 1:


Input: root = [4,2,7,1,3,6,9]
Output: [4,7,2,9,6,3,1]
Example 2:


Input: root = [2,1,3]
Output: [2,3,1]
Example 3:

Input: root = []
Output: []


Constraints:

The number of nodes in the tree is in the range [0, 100].
-100 <= Node.val <= 100

Seen this question in a real interview before?
1/6
Yes
No
Accepted
3,035,627/3.8M
Acceptance Rate
80.0%

"""
from operator import invert
from typing import Optional


# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def swap_children(node: TreeNode):
    node.left, node.right = node.right, node.left

def invert_tree(root: Optional[TreeNode]):
    if root is None:
        return None

    swap_children(root)
    root.left = invert_tree(root.left)
    root.right = invert_tree(root.right)
    return root

class Solution:
    def invertTree(self, root: Optional[TreeNode]) -> Optional[TreeNode]:
        return invert_tree(root)