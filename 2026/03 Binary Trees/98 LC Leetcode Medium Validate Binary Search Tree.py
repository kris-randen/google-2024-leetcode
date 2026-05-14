"""

98. Validate Binary Search Tree
Solved
Medium
Topics
conpanies icon
Companies
Given the root of a binary tree, determine if it is a valid binary search tree (BST).

A valid BST is defined as follows:

The left subtree of a node contains only nodes with keys strictly less than the node's key.
The right subtree of a node contains only nodes with keys strictly greater than the node's key.
Both the left and right subtrees must also be binary search trees.


Example 1:


Input: root = [2,1,3]
Output: true
Example 2:


Input: root = [5,1,4,null,null,3,6]
Output: false
Explanation: The root node's value is 5 but its right child's value is 4.


Constraints:

The number of nodes in the tree is in the range [1, 104].
-231 <= Node.val <= 231 - 1

"""

from typing import Optional, Iterable, List


# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def inorder_nodes(root: Optional[TreeNode]) -> Iterable[TreeNode]:
    if root is None:
        return

    yield from inorder_nodes(root.left)
    yield root
    yield from inorder_nodes(root.right)

Frame = tuple[Optional[TreeNode], bool]

def inorder_iter(root: Optional[TreeNode]) -> Iterable[TreeNode]:
    stack: List[Frame] = [(root, False)]

    while stack:
        node, emit = stack.pop()

        if node is None:
            continue

        if emit:
            yield node
        else:
            stack.append((node.right, False))
            stack.append((node, True))
            stack.append((node.left, False))

def values_tree(root: Optional[TreeNode]):
    return list(node.val for node in inorder_iter(root))

def is_sorted(vs) -> bool:
    return all(u < v for u, v in zip(vs, vs[1:]))

def validate_tree(root: Optional[TreeNode]):
    return is_sorted(values_tree(root))

class Solution:
    def isValidBST(self, root: Optional[TreeNode]) -> bool:
        return validate_tree(root)
