"""

270. Closest Binary Search Tree Value
Solved
Easy
Topics
conpanies icon
Companies
Given the root of a binary search tree and a target value, return the value in the BST that is closest to the target. If there are multiple answers, print the smallest.



Example 1:


Input: root = [4,2,5,1,3], target = 3.714286
Output: 4
Example 2:

Input: root = [1], target = 4.428571
Output: 1


Constraints:

The number of nodes in the tree is in the range [1, 104].
0 <= Node.val <= 109
-109 <= target <= 109

Seen this question in a real interview before?
1/6
Yes
No
Accepted
453,548/921.7K
Acceptance Rate
49.2%

"""


from typing import Optional


# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def closest_long(root: Optional[TreeNode], target: float):
    def find(node: Optional[TreeNode]) -> tuple[float, int]:
        if node is None:
            return float('inf'), float('inf')

        here = abs(node.val - target), node.val
        left = find(node.left)
        right = find(node.right)

        return min(here, left, right)

    return find(root)[1]

def closest(root: Optional[TreeNode], target: float):
    def find(node: Optional[TreeNode]) -> tuple[float, int]:
        if node is None:
            return float('inf'), float('inf')

        if node.val == target:
            return 0, node.val

        here = abs(node.val - target), node.val
        child = find(node.left) if target < node.val else find(node.right)

        return min(here, child)
    return find(root)[1]

class Solution:
    def closestValue(self, root: Optional[TreeNode], target: float) -> int:
        return closest_long(root, target)
