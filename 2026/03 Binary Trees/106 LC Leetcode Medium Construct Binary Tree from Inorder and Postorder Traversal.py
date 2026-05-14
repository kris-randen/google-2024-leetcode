"""

106. Construct Binary Tree from Inorder and Postorder Traversal
Solved
Medium

Given two integer arrays inorder and postorder where inorder is the inorder traversal of a binary tree and postorder is the postorder traversal of the same tree, construct and return the binary tree.


Example 1:


Input: inorder = [9,3,15,20,7], postorder = [9,15,7,20,3]
Output: [3,9,20,null,null,15,7]
Example 2:

Input: inorder = [-1], postorder = [-1]
Output: [-1]


Constraints:

1 <= inorder.length <= 3000
postorder.length == inorder.length
-3000 <= inorder[i], postorder[i] <= 3000
inorder and postorder consist of unique values.
Each value of postorder also appears in inorder.
inorder is guaranteed to be the inorder traversal of the tree.
postorder is guaranteed to be the postorder traversal of the tree.

Seen this question in a real interview before?
1/6
Yes
No
Accepted
954,035/1.4M
Acceptance Rate
68.5%

"""

from typing import List, Optional

# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def tree_from(inorder: List[int], postorder: List[int]):
    ind = len(postorder) - 1

    def rec(start, end):
        nonlocal ind

        if end == start:
            return None

        val = postorder[ind]
        ind -= 1
        mid = inorder.index(val)

        root = TreeNode(val)
        root.right = rec(mid + 1, end)
        root.left = rec(start, mid)

        return root

    return rec(0, len(postorder))

class Solution:
    def buildTree(self, inorder: List[int], postorder: List[int]) -> Optional[TreeNode]:
        return tree_from(inorder, postorder)