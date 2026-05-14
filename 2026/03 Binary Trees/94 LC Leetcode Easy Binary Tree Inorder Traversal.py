"""

94. Binary Tree Inorder Traversal
Solved
Easy
Topics
conpanies icon
Companies
Given the root of a binary tree, return the inorder traversal of its nodes' values.



Example 1:

Input: root = [1,null,2,3]

Output: [1,3,2]

Explanation:



Example 2:

Input: root = [1,2,3,4,5,null,8,null,null,6,7,9]

Output: [4,2,6,5,7,1,3,9,8]

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
3,701,663/4.6M
Acceptance Rate
80.0%

"""
from typing import Optional, List, Iterable


# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def inorder_nodes(root: Optional[TreeNode]):
    if root is None:
        return

    yield from inorder_nodes(root.left)
    yield root
    yield from inorder_nodes(root.right)

def values_iter(nodes: Iterable[TreeNode]):
    return (node.val for node in nodes)

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


class Solution:
    def inorderTraversal(self, root: Optional[TreeNode]) -> List[int]:
        return \
        (
            list(
                values_iter(
                    inorder_iter(root)
                )
            )
        )
