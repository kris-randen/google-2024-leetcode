"""

114. Flatten Binary Tree to Linked List
Medium

The "linked list" should use the same TreeNode class where the right child pointer points to the next node in the list and the left child pointer is always null.
The "linked list" should be in the same order as a pre-order traversal of the binary tree.


Example 1:

Input: root = [1,2,5,3,4,null,6]
Output: [1,null,2,null,3,null,4,null,5,null,6]
Example 2:

Input: root = []
Output: []
Example 3:

Input: root = [0]
Output: [0]


Constraints:

The number of nodes in the tree is in the range [0, 2000].
-100 <= Node.val <= 100


Follow up: Can you flatten the tree in-place (with O(1) extra space)?

"""
from typing import Optional


# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def flat(node):
    match node:
        case None:
            return None, None
        case TreeNode(left=left, right=right):
            lh, lt = flat(left)
            rh, rt = flat(right)
            node.left = None
            if not left and not right:
                return node, node
            if left and right:
                node.right = lh
                lt.right = rh
                return node, rt
            if not left:
                node.right = rh
                return node, rt
            if not right:
                node.right = lh
                return node, lt

def flatten(root: Optional[TreeNode]) -> None:
    h, t = flat(root)