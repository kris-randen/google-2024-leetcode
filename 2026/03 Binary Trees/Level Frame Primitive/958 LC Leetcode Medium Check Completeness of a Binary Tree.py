"""

958. Check Completeness of a Binary Tree
Medium

Given the root of a binary tree, determine if it is a complete binary tree.

In a complete binary tree, every level, except possibly the last, is completely filled, and all nodes in the last level are as far left as possible. It can have between 1 and 2h nodes inclusive at the last level h.



Example 1:


Input: root = [1,2,3,4,5,6]
Output: true
Explanation: Every level before the last is full (ie. levels with node-values {1} and {2, 3}), and all nodes in the last level ({4, 5, 6}) are as far left as possible.
Example 2:


Input: root = [1,2,3,4,5,null,7]
Output: false
Explanation: The node with value 7 isn't as far left as possible.


Constraints:

The number of nodes in the tree is in the range [1, 100].
1 <= Node.val <= 1000

Seen this question in a real interview before?
1/6
Yes
No
Accepted
321,587/543.6K
Acceptance Rate
59.2%

"""
from collections import deque
from typing import Optional


# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def bfs_with_pos(root: Optional[TreeNode]):
    if root is None:
        return

    q = deque([(1, root)])

    while q:
        index, node = q.popleft()
        yield index, node

        if node.left:
            q.append((2 * index, node.left))
        if node.right:
            q.append((2 * index + 1, node.right))

def is_complete(root: Optional[TreeNode]):
    bfs_iter = bfs_with_pos(root)
    last, _ = next(bfs_iter)

    for index, _ in bfs_iter:
        if not index - last == 1:
            return False
        last = index

    return True

class Solution:
    def isCompleteTree(self, root: Optional[TreeNode]) -> bool:
        return is_complete(root)
