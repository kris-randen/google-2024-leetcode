"""

513. Find Bottom Left Tree Value
Medium

Given the root of a binary tree, return the leftmost value in the last row of the tree.



Example 1:


Input: root = [2,1,3]
Output: 1
Example 2:


Input: root = [1,2,3,4,null,5,6,null,null,7]
Output: 7


Constraints:

The number of nodes in the tree is in the range [1, 104].
-231 <= Node.val <= 231 - 1

Seen this question in a real interview before?
1/6
Yes
No
Accepted
444,709/615.1K
Acceptance Rate
72.3%

"""
from collections import deque
from typing import Optional, List, Iterator


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


def values(levels: Iterator[List[TreeNode]]) -> List[List[int]]:
    return [[node.val for node in level] for level in levels]

def left_side(level_values: List[List[int]]) -> List[int]:
    return [level[0] for level in level_values]

class Solution:
    def findBottomLeftValue(self, root: Optional[TreeNode]) -> int:
        return left_side(values(level_nodes(root)))[-1]
