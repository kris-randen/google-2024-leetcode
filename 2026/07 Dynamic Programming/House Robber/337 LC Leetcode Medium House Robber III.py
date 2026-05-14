"""

337. House Robber III
Solved
Medium

The thief has found himself a new place for his thievery again. There is only one entrance to this area, called root.

Besides the root, each house has one and only one parent house. After a tour, the smart thief realized that all houses in this place form a binary tree. It will automatically contact the police if two directly-linked houses were broken into on the same night.

Given the root of the binary tree, return the maximum amount of money the thief can rob without alerting the police.



Example 1:


Input: root = [3,2,3,null,3,null,1]
Output: 7
Explanation: Maximum amount of money the thief can rob = 3 + 3 + 1 = 7.
Example 2:


Input: root = [3,4,5,1,3,null,1]
Output: 9
Explanation: Maximum amount of money the thief can rob = 4 + 5 = 9.


Constraints:

The number of nodes in the tree is in the range [1, 104].
0 <= Node.val <= 104

Seen this question in a real interview before?
1/6
Yes
No
Accepted
509,191/911.2K
Acceptance Rate
55.9%

"""

from functools import lru_cache
from typing import Optional


# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def max_loot_bst(root: Optional[TreeNode]) -> int:
    @lru_cache()
    def loot(node: Optional[TreeNode], cant_rob: bool) -> int:
        if node is None:
            return 0
        if cant_rob:
            return loot(node.left, cant_rob=False) + loot(node.right, cant_rob=False)
        else:
            return max(
                node.val + loot(node.left, cant_rob=True) + loot(node.right, cant_rob=True),
                loot(node.left, cant_rob=False) + loot(node.right, cant_rob=False)
            )

    return loot(root, cant_rob=False)


class Solution:
    def rob(self, root: Optional[TreeNode]) -> int:
        return max_loot_bst(root)
