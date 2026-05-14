"""

1305. All Elements in Two Binary Search Trees
Medium

Hint
Given two binary search trees root1 and root2, return a list containing all the integers from both trees sorted in ascending order.



Example 1:


Input: root1 = [2,1,4], root2 = [1,0,3]
Output: [0,1,1,2,3,4]
Example 2:


Input: root1 = [1,null,8], root2 = [8,1]
Output: [1,1,8,8]


Constraints:

The number of nodes in each tree is in the range [0, 5000].
-105 <= Node.val <= 105

Seen this question in a real interview before?
1/6
Yes
No
Accepted
263,279/328.1K
Acceptance Rate
80.3%

"""
from tarfile import StreamError
from typing import Optional, List, Iterator


# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def inorder_nodes(root: Optional[TreeNode]) -> Iterator[TreeNode]:
    if root is None:
        return

    yield from inorder_nodes(root.left)
    yield root
    yield from inorder_nodes(root.right)

def drain(node, nodes):
    while node is not None:
        yield node
        node = next(nodes, None)

def merge(inorder_a: Iterator[TreeNode], inorder_b: Iterator[TreeNode]) -> Iterator[TreeNode]:
    node_a, node_b = next(inorder_a, None), next(inorder_b, None)

    while node_a is not None and node_b is not None:
        if node_a.val <= node_b.val:
            yield node_a
            node_a = next(inorder_a, None)
        else:
            yield node_b
            node_b = next(inorder_b, None)

    yield from drain(node_a, inorder_a)
    yield from drain(node_b, inorder_b)

class Solution:
    def getAllElements(self, root1: Optional[TreeNode], root2: Optional[TreeNode]) -> List[int]:
        return \
        (
            list(
                node.val for node in
                merge(
                    inorder_nodes(root1),
                    inorder_nodes(root2)
                )
            )
        )
