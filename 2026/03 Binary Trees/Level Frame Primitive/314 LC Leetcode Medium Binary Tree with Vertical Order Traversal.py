"""

314. Binary Tree Vertical Order Traversal
Solved
Medium

Given the root of a binary tree, return the vertical order traversal of its nodes' values. (i.e., from top to bottom, column by column).

If two nodes are in the same row and column, the order should be from left to right.



Example 1:


Input: root = [3,9,20,null,null,15,7]
Output: [[9],[3,15],[20],[7]]
Example 2:


Input: root = [3,9,8,4,0,1,7]
Output: [[4],[9],[3,0,1],[8],[7]]
Example 3:


Input: root = [1,2,3,4,10,9,11,null,5,null,null,null,null,null,null,null,6]
Output: [[4],[2,5],[1,10,9,6],[3],[11]]


Constraints:

The number of nodes in the tree is in the range [0, 100].
-100 <= Node.val <= 100

Seen this question in a real interview before?
1/6
Yes
No
Accepted
596,742/1M
Acceptance Rate
57.8%

"""
from collections import deque, defaultdict
from typing import Optional, List


# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def bfs_with_pos(root: Optional[TreeNode]):
    if root is None:
        return

    q = deque([(0, 0, root)])

    while q:
        col, depth, node = q.popleft()
        yield col, depth, node
        if node.left:
            q.append((col - 1, depth + 1, node.left))
        if node.right:
            q.append((col + 1, depth + 1, node.right))

def vertical_order(bfs_with_pos):
    cols = defaultdict(list)

    for col, depth, node in bfs_with_pos:
        cols[col].append((col, depth, node))

    return \
    [
        cols[c] for
        c in sorted(cols)
    ]

def values(levels):
    return \
    [
        [node.val for _, _, node in level]
        for level in levels
    ]

class Solution:
    def verticalOrder(self, root: Optional[TreeNode]) -> List[List[int]]:
        return \
        (
            values(
                vertical_order(
                    bfs_with_pos(root)
                )
            )
        )


