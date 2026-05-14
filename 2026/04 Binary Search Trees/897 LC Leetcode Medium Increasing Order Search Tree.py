"""

897. Increasing Order Search Tree
Easy

Given the root of a binary search tree, rearrange the tree in in-order so that the leftmost node in the tree is now the root of the tree, and every node has no left child and only one right child.



Example 1:


Input: root = [5,3,6,2,4,null,8,1,null,null,null,7,9]
Output: [1,null,2,null,3,null,4,null,5,null,6,null,7,null,8,null,9]
Example 2:


Input: root = [5,1,7]
Output: [1,null,5,null,7]


Constraints:

The number of nodes in the given tree will be in the range [1, 100].
0 <= Node.val <= 1000

Seen this question in a real interview before?
1/6
Yes
No
Accepted
339,512/429.9K
Acceptance Rate
79.0%

"""

from __future__ import annotations
from typing import Optional, Iterator


# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def reverse_order(root: Optional[TreeNode]) -> Iterator[TreeNode]:
    if root is None:
        return

    yield from reverse_order(root.right)
    yield root
    yield from reverse_order(root.left)

def inorder(root: Optional[TreeNode]) -> Iterator[TreeNode]:
    if root is None:
        return

    yield from inorder(root.left)
    yield root
    yield from inorder(root.right)



def increasing_reverse(root: Optional[TreeNode]) -> Optional[TreeNode]:
    if root is None:
        return None

    prev = None

    for node in list(reverse_order(root)):
        node.left = None
        node.right = prev
        prev = node

    return prev

def increasing(root: Optional[TreeNode]) -> Optional[TreeNode]:
    dummy = tail = TreeNode()

    for node in inorder(root):
        tail.right = node
        node.left = None
        tail = node

    tail.left = None
    return dummy.right


class Solution:
    def increasingBST(self, root: Optional[TreeNode]) -> Optional[TreeNode]:
        return increasing(root)


