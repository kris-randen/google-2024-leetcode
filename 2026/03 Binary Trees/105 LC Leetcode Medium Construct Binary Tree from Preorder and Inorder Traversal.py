"""

105. Construct Binary Tree from Preorder and Inorder Traversal
Solved
Medium
Topics
conpanies icon
Companies
Given two integer arrays preorder and inorder where preorder is the preorder traversal of a binary tree and inorder is the inorder traversal of the same tree, construct and return the binary tree.



Example 1:


Input: preorder = [3,9,20,15,7], inorder = [9,3,15,20,7]
Output: [3,9,20,null,null,15,7]
Example 2:

Input: preorder = [-1], inorder = [-1]
Output: [-1]


Constraints:

1 <= preorder.length <= 3000
inorder.length == preorder.length
-3000 <= preorder[i], inorder[i] <= 3000
preorder and inorder consist of unique values.
Each value of inorder also appears in preorder.
preorder is guaranteed to be the preorder traversal of the tree.
inorder is guaranteed to be the inorder traversal of the tree.

Seen this question in a real interview before?
1/6
Yes
No
Accepted
1,867,455/2.7M
Acceptance Rate
68.7%

"""

from typing import List, Optional


# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def tree_from(preorder: List[int], inorder: List[int]) -> Optional[TreeNode]:
    pre_ind = 0
    def rec(start: int, end: int) -> Optional[TreeNode]:
        nonlocal  pre_ind

        if start == end:
            return None

        val = preorder[pre_ind]
        pre_ind += 1
        mid = inorder.index(val)

        root = TreeNode(val)
        root.left = rec(start, mid)
        root.right = rec(mid + 1, end)
        return root

    return rec(0, len(preorder))

class Solution:
    def buildTree(self, preorder: List[int], inorder: List[int]) -> Optional[TreeNode]:
        return tree_from(preorder, inorder)
