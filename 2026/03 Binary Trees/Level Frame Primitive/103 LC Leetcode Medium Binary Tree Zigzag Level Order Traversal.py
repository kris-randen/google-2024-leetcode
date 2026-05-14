"""

103. Binary Tree Zigzag Level Order Traversal
Solved
Medium

Given the root of a binary tree, return the zigzag level order traversal of its nodes' values. (i.e., from left to right, then right to left for the next level and alternate between).


Example 1:


Input: root = [3,9,20,null,null,15,7]
Output: [[3],[20,9],[15,7]]
Example 2:

Input: root = [1]
Output: [[1]]
Example 3:

Input: root = []
Output: []


Constraints:

The number of nodes in the tree is in the range [0, 2000].
-100 <= Node.val <= 100

Seen this question in a real interview before?
1/6
Yes
No
Accepted
1,781,104/2.8M
Acceptance Rate
63.6%

"""
from collections import deque
from typing import List, Optional, Iterator


# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def level_nodes(root: Optional[TreeNode]) -> Iterator[List[TreeNode]]:
    if root is None:
        return

    q = deque([root])

    while q:
        level_size = len(q)
        level = []

        for _ in range(level_size):
            node = q.popleft()
            level.append(node)

            if node.left:
                q.append(node.left)
            if node.right:
                q.append(node.right)

        yield level

def level_values(levels: Iterator[List[TreeNode]]) -> Iterator[List[int]]:
    return ([node.val for node in level] for level in levels)

def zigzag(levels: Iterator[List[int]]) -> List[List[int]]:
    return \
    [
        (
            level if i % 2 == 0 else list(reversed(level))
        )
        for i, level in enumerate(levels)
    ]

class Solution:
    def zigzagLevelOrder(self, root: Optional[TreeNode]) -> List[List[int]]:
        return zigzag(level_values(level_nodes(root)))
