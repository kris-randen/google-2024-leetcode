"""

965. Univalued Binary Tree
Easy

A binary tree is uni-valued if every node in the tree has the same value.

Given the root of a binary tree, return true if the given tree is uni-valued, or false otherwise.



Example 1:


Input: root = [1,1,1,1,1,null,1]
Output: true
Example 2:


Input: root = [2,2,2,5,2]
Output: false


Constraints:

The number of nodes in the tree is in the range [1, 100].
0 <= Node.val < 100

Seen this question in a real interview before?
1/6
Yes
No
Accepted
276,582/378.8K
Acceptance Rate
73.0%

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

def values_iter(nodes: Iterable[TreeNode]):
    return (node.val for node in nodes)

class Solution:
    def isUnivalTree(self, root: Optional[TreeNode]) -> bool:
        if root is None: return False
        return \
        (
            all(
                val == root.val
                for val in
                values_iter(
                    inorder_iter(root)
                )
            )
        )
