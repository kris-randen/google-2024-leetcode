"""

515. Find Largest Value in Each Tree Row
Solved
Medium

Given the root of a binary tree, return an array of the largest value in each row of the tree (0-indexed).



Example 1:


Input: root = [1,3,2,5,3,null,9]
Output: [1,3,9]
Example 2:

Input: root = [1,2,3]
Output: [1,3]


Constraints:

The number of nodes in the tree will be in the range [0, 104].
-231 <= Node.val <= 231 - 1

Seen this question in a real interview before?
1/6
Yes
No
Accepted
521,615/786.6K
Acceptance Rate
66.3%

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
        level, level_size = [], len(q)

        for _ in range(level_size):
            node = q.popleft()
            level.append(node)

            if node.left:
                q.append(node.left)
            if node.right:
                q.append(node.right)

        yield level

def values(levels: Iterator[List[TreeNode]]) -> Iterator[List[int]]:
    return ([node.val for node in level] for level in levels)

class Solution:
    def largestValues(self, root: Optional[TreeNode]) -> List[int]:
        return list(max(level) for level in values(level_nodes(root)))
