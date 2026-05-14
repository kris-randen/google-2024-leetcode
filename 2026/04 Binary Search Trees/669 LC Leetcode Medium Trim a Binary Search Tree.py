"""

669. Trim a Binary Search Tree
Medium

Given the root of a binary search tree and the lowest and highest boundaries as low and high, trim the tree so that all its elements lies in [low, high]. Trimming the tree should not change the relative structure of the elements that will remain in the tree (i.e., any node's descendant should remain a descendant). It can be proven that there is a unique answer.

Return the root of the trimmed binary search tree. Note that the root may change depending on the given bounds.



Example 1:


Input: root = [1,0,2], low = 1, high = 2
Output: [1,null,2]
Example 2:


Input: root = [3,0,4,null,2,null,null,1], low = 1, high = 3
Output: [3,2,null,1]


Constraints:

The number of nodes in the tree is in the range [1, 104].
0 <= Node.val <= 104
The value of each node in the tree is unique.
root is guaranteed to be a valid binary search tree.
0 <= low <= high <= 104

Seen this question in a real interview before?
1/6
Yes
No
Accepted
348,473/522.3K
Acceptance Rate
66.7%

"""

from typing import Optional


# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def trim(root: Optional[TreeNode], lo: int, hi: int) -> Optional[TreeNode]:
    if root is None:
        return None

    val, left, right = root.val, root.left, root.right

    if val < lo:
        return trim(right, lo, hi)
    if val > hi:
        return trim(left, lo, hi)

    root.left = trim(left, lo, hi)
    root.right = trim(right, lo, hi)

    return root

class Solution:
    def trimBST(self, root: Optional[TreeNode], low: int, high: int) -> Optional[TreeNode]:
        return trim(root, low, high)
