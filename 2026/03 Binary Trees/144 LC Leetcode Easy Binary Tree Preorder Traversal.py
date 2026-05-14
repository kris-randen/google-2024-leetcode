"""

144. Binary Tree Preorder Traversal
Solved
Easy
Given the root of a binary tree, return the preorder traversal of its nodes' values.



Example 1:

Input: root = [1,null,2,3]

Output: [1,2,3]

Explanation:



Example 2:

Input: root = [1,2,3,4,5,null,8,null,null,6,7,9]

Output: [1,2,4,5,6,7,3,8,9]

Explanation:



Example 3:

Input: root = []

Output: []

Example 4:

Input: root = [1]

Output: [1]



Constraints:

The number of nodes in the tree is in the range [0, 100].
-100 <= Node.val <= 100


Follow up: Recursive solution is trivial, could you do it iteratively?


Seen this question in a real interview before?
1/6
Yes
No
Accepted
2,440,234/3.2M
Acceptance Rate
75.6%

"""
from tkinter import Frame
from typing import Optional, List, Iterable


# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

Frame = tuple[Optional[TreeNode], bool]


def preorder_nodes(root: Optional[TreeNode]):
    if root is None:
        return

    yield root
    yield from preorder_nodes(root.left)
    yield from preorder_nodes(root.right)

def values_iter(nodes: Iterable[TreeNode]):
    return (node.val for node in nodes)

def preorder_iter(root: Optional[TreeNode]) -> Iterable[TreeNode]:
    stack: List[Frame] = [(root, False)]

    while stack:
        node, emit = stack.pop()

        if node is None:
            continue

        if emit:
            yield node
        else:
            stack.append((node.right, False))
            stack.append((node.left, False))
            stack.append((node, True))



class Solution:
    def preorderTraversal(self, root: Optional[TreeNode]) -> List[int]:
        return \
        (
            list(
                values_iter(
                    preorder_nodes(root)
                )
            )
        )
