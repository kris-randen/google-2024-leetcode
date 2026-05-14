"""

700. Search in a Binary Search Tree
Easy

You are given the root of a binary search tree (BST) and an integer val.

Find the node in the BST that the node's value equals val and return the subtree rooted with that node. If such a node does not exist, return null.



Example 1:


Input: root = [4,2,7,1,3], val = 2
Output: [2,1,3]
Example 2:


Input: root = [4,2,7,1,3], val = 5
Output: []


Constraints:

The number of nodes in the tree is in the range [1, 5000].
1 <= Node.val <= 107
root is a binary search tree.
1 <= val <= 107

Seen this question in a real interview before?
1/6
Yes
No
Accepted
1,388,350/1.7M
Acceptance Rate
82.7%

"""


from typing import Optional


# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def get_key(root: Optional[TreeNode], val: int) -> Optional[TreeNode]:
    if root is None:
        return None

    if val == root.val:
        return root
    elif val < root.val:
        return get_key(root.left, val)
    else:
        return get_key(root.right, val)


class Solution:
    def searchBST(self, root: Optional[TreeNode], val: int) -> Optional[TreeNode]:
        return get_key(root, val)
