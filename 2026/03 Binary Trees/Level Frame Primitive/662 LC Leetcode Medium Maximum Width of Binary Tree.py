"""

662. Maximum Width of Binary Tree
Medium

Given the root of a binary tree, return the maximum width of the given tree.

The maximum width of a tree is the maximum width among all levels.

The width of one level is defined as the length between the end-nodes (the leftmost and rightmost non-null nodes), where the null nodes between the end-nodes that would be present in a complete binary tree extending down to that level are also counted into the length calculation.

It is guaranteed that the answer will in the range of a 32-bit signed integer.



Example 1:


Input: root = [1,3,2,5,3,null,9]
Output: 4
Explanation: The maximum width exists in the third level with length 4 (5,3,null,9).
Example 2:


Input: root = [1,3,2,5,null,null,9,6,null,7]
Output: 7
Explanation: The maximum width exists in the fourth level with length 7 (6,null,null,null,null,null,7).
Example 3:


Input: root = [1,3,2,5]
Output: 2
Explanation: The maximum width exists in the second level with length 2 (3,2).


Constraints:

The number of nodes in the tree is in the range [1, 3000].
-100 <= Node.val <= 100

Seen this question in a real interview before?
1/6
Yes
No
Accepted
595,330/1.3M
Acceptance Rate
45.6%

"""
from collections import deque
from typing import Optional


# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def levels_with_pos(root: Optional[TreeNode]):
    if root is None:
        return

    q = deque([(0, 1, root)])

    while q:
        level, level_size = [], len(q)
        for _ in range(level_size):
            row, idx, node = q.popleft()
            level.append((row, idx, node))

            if node.left:
                q.append((row + 1, 2 * idx, node.left))
            if node.right:
                q.append((row + 1, 2 * idx + 1, node.right))

        yield level

def level_pos(level):
    row, idx, _ = level
    return idx - 2 ** row

def widths(levels):
    return [(level_pos(level[-1]) - level_pos(level[0])) + 1 for level in levels]



class Solution:
    def widthOfBinaryTree(self, root: Optional[TreeNode]) -> int:
        return max(widths(levels_with_pos(root)))
