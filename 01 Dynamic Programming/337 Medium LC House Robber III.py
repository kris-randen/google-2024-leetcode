"""

337. House Robber III
Solved
Medium
Topics
Companies
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
1/5
Yes
No
Accepted
395.4K
Submissions
726.8K
Acceptance Rate
54.4%

Runtime 36 ms Beats 95.10%
Memory 20.56 MB Beats 7.83%

"""

from functools import lru_cache

def loot_street(root):
    @lru_cache(None)
    def loot(house, cant_rob=False):
        if not house: return 0
        clr = loot(house.left, False) +\
              loot(house.right, False)
        if cant_rob: return clr

        rlr = house.val +\
              loot(house.left, True) +\
              loot(house.right, True)
        return max(clr, rlr)
    return loot(root)
