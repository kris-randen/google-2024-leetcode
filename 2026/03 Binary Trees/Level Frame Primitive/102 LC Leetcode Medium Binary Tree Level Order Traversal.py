"""

102. Binary Tree Level Order Traversal
Solved
Medium

Given the root of a binary tree, return the level order traversal of its nodes' values. (i.e., from left to right, level by level).



Example 1:


Input: root = [3,9,20,null,null,15,7]
Output: [[3],[9,20],[15,7]]
Example 2:

Input: root = [1]
Output: [[1]]
Example 3:

Input: root = []
Output: []


Constraints:

The number of nodes in the tree is in the range [0, 2000].
-1000 <= Node.val <= 1000

Seen this question in a real interview before?
1/6
Yes
No
Accepted
3,408,783/4.7M
Acceptance Rate
72.6%

"""
from collections import deque
from typing import Optional, List, Iterator


# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def level_nodes(root: Optional[TreeNode]) -> Iterator[List[int]]:
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

def level_values(root: Optional[TreeNode]) -> List[List[int]]:
    return [[node.val for node in level] for level in level_nodes(root)]


class Solution:
    def levelOrder(self, root: Optional[TreeNode]) -> List[List[int]]:
        return level_values(root)
