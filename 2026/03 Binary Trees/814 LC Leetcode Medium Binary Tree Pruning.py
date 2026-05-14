"""

814. Binary Tree Pruning
Medium

Given the root of a binary tree, return the same tree where every subtree (of the given tree) not containing a 1 has been removed.

A subtree of a node node is node plus every node that is a descendant of node.



Example 1:


Input: root = [1,null,0,0,1]
Output: [1,null,0,null,1]
Explanation:
Only the red nodes satisfy the property "every subtree not containing a 1".
The diagram on the right represents the answer.
Example 2:


Input: root = [1,0,1,0,0,0,1]
Output: [1,null,1,null,1]
Example 3:


Input: root = [1,1,0,1,1,0,1,0]
Output: [1,1,0,1,1,null,1]


Constraints:

The number of nodes in the tree is in the range [1, 200].
Node.val is either 0 or 1.

Seen this question in a real interview before?
1/6
Yes
No
Accepted
287,804/397K
Acceptance Rate
72.5%

"""
from email.utils import rfc2231_continuation
from typing import Optional

# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def prune_tree(root: Optional[TreeNode]) -> Optional[TreeNode]:
    def dfs(node:Optional[TreeNode]) -> tuple[bool, Optional[TreeNode]]:
        if node is None:
            return False, None

        l_contains, left = dfs(node.left)
        r_contains, right = dfs(node.right)

        node.left = left
        node.right = right

        contains = l_contains or r_contains or (node.val == 1)

        return (contains, node) if contains else (False, None)

    return dfs(root)[1]

class Solution:
    def pruneTree(self, root: Optional[TreeNode]) -> Optional[TreeNode]:
        return prune_tree(root)
