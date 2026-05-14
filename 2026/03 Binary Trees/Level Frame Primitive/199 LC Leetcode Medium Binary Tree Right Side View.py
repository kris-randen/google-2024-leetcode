"""

199. Binary Tree Right Side View
Solved
Medium
Topics
conpanies icon
Companies
Given the root of a binary tree, imagine yourself standing on the right side of it, return the values of the nodes you can see ordered from top to bottom.



Example 1:

Input: root = [1,2,3,null,5,null,4]

Output: [1,3,4]

Explanation:



Example 2:

Input: root = [1,2,3,4,null,null,null,5]

Output: [1,3,4,5]

Explanation:



Example 3:

Input: root = [1,null,3]

Output: [1,3]

Example 4:

Input: root = []

Output: []



Constraints:

The number of nodes in the tree is in the range [0, 100].
-100 <= Node.val <= 100

Seen this question in a real interview before?
1/6
Yes
No
Accepted
2,233,243/3.2M
Acceptance Rate
70.1%

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

def values(levels: Iterator[List[TreeNode]]) -> List[List[int]]:
    return [[node.val for node in level] for level in levels]

def right_side(level_values: List[List[int]]):
    return [level[-1] for level in level_values]

class Solution:
    def rightSideView(self, root: Optional[TreeNode]) -> List[int]:
        return right_side(values(level_nodes(root)))
