"""

145. Binary Tree Postorder Traversal
Solved
Easy

Given the root of a binary tree, return the postorder traversal of its nodes' values.



Example 1:

Input: root = [1,null,2,3]

Output: [3,2,1]

Explanation:



Example 2:

Input: root = [1,2,3,4,5,null,8,null,null,6,7,9]

Output: [4,6,7,5,2,9,8,3,1]

Explanation:



Example 3:

Input: root = []

Output: []

Example 4:

Input: root = [1]

Output: [1]



Constraints:

The number of the nodes in the tree is in the range [0, 100].
-100 <= Node.val <= 100


Follow up: Recursive solution is trivial, could you do it iteratively?

Seen this question in a real interview before?
1/6
Yes
No
Accepted
1,966,526/2.5M
Acceptance Rate
78.0%

"""
from idlelib.tree import TreeNode
from typing import Optional, List, Iterable

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def postorder_nodes(root: Optional[TreeNode]) -> Iterable[TreeNode]:
    if root is None:
        return

    yield from postorder_nodes(root.left)
    yield from postorder_nodes(root.right)
    yield root

def values_iter(nodes: Iterable[TreeNode]):
    return (node.val for node in nodes)

Frame = tuple[Optional[TreeNode], bool]

def postorder_iter(root: Optional[TreeNode]) -> Iterable[TreeNode]:
    stack: List[Frame] = [(root, False)]

    while stack:
        node, emit = stack.pop()

        if node is None:
            continue

        if emit:
            yield node
        else:
            stack.append((node, True))
            stack.append((node.right, False))
            stack.append((node.left, False))


class Solution:
    def postorderTraversal(self, root: Optional[TreeNode]) -> List[int]:
        return \
        (
            list(
                values_iter(
                    postorder_iter(root)
                )
            )
        )
