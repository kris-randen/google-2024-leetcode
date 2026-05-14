"""

538. Convert BST to Greater Tree
Medium

Given the root of a Binary Search Tree (BST), convert it to a Greater Tree such that every key of the original BST is changed to the original key plus the sum of all keys greater than the original key in BST.

As a reminder, a binary search tree is a tree that satisfies these constraints:

The left subtree of a node contains only nodes with keys less than the node's key.
The right subtree of a node contains only nodes with keys greater than the node's key.
Both the left and right subtrees must also be binary search trees.


Example 1:


Input: root = [4,1,6,0,2,5,7,null,null,null,3,null,null,null,8]
Output: [30,36,21,36,35,26,15,null,null,null,33,null,null,null,8]
Example 2:

Input: root = [0,null,1]
Output: [1,null,1]


Constraints:

The number of nodes in the tree is in the range [0, 104].
-104 <= Node.val <= 104
All the values in the tree are unique.
root is guaranteed to be a valid binary search tree.


Note: This question is the same as 1038: https://leetcode.com/problems/binary-search-tree-to-greater-sum-tree/


Seen this question in a real interview before?
1/6
Yes
No
Accepted
357,146/498.7K
Acceptance Rate
71.6%

"""

from typing import Optional, Iterable, Iterator, List


# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def reverse_inorder_nodes(root: Optional[TreeNode]) -> Iterator[TreeNode]:
    if root is None:
        return

    yield from reverse_inorder_nodes(root.right)
    yield root
    yield from reverse_inorder_nodes(root.left)


Frame = tuple[Optional[TreeNode], bool]

def reverse_inorder_iter(root: Optional[TreeNode]) -> Iterator[TreeNode]:
    stack: List[Frame] = [(root, False)]

    while stack:
        node, emit = stack.pop()

        if node is None:
            continue

        if emit:
            yield node
        else:
            stack.append((node.left, False))
            stack.append((node, True))
            stack.append((node.right, False))

def to_greater_tree(root: Optional[TreeNode]):
    total = 0
    for node in reverse_inorder_iter(root):
        total += node.val
        node.val = total
    return root


class Solution:
    def convertBST(self, root: Optional[TreeNode]) -> Optional[TreeNode]:
        return to_greater_tree(root)
