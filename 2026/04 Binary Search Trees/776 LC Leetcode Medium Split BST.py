"""

776. Split BST
Medium

Given the root of a binary search tree (BST) and an integer target, split the tree into two subtrees where the first subtree has nodes that are all smaller or equal to the target value, while the second subtree has all nodes that are greater than the target value. It is not necessarily the case that the tree contains a node with the value target.

Additionally, most of the structure of the original tree should remain. Formally, for any child c with parent p in the original tree, if they are both in the same subtree after the split, then node c should still have the parent p.

Return an array of the two roots of the two subtrees in order.



Example 1:


Input: root = [4,2,6,1,3,5,7], target = 2
Output: [[2,1],[4,3,6,null,null,5,7]]
Example 2:

Input: root = [1], target = 1
Output: [[1],[]]


Constraints:

The number of nodes in the tree is in the range [1, 50].
0 <= Node.val, target <= 1000

Seen this question in a real interview before?
1/6
Yes
No
Accepted
112,378/136.8K
Acceptance Rate
82.2%

"""


from typing import Optional, List


# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def clone(root: Optional[TreeNode]):
    if root is None:
        return None

    return TreeNode(root.val, clone(root.left), clone(root.right))

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

def split_trim(root: Optional[TreeNode], target: int) -> tuple[Optional[TreeNode], Optional[TreeNode]]:
    less, great = root, clone(root)
    return trim(less, float('-inf'), target), trim(great, target + 1, float('inf'))


def split(root: Optional[TreeNode], target: int):
    if root is None:
        return None, None

    val, left, right = root.val, root.left, root.right

    if val == target:
        root.right = None
        return root, right

    if val < target:
        less, more = split(right, target)
        root.right = less
        return root, more
    else:
        less, more = split(left, target)
        root.left = more
        return less, root

class Solution:
    def splitBST(self, root: Optional[TreeNode], target: int) -> List[Optional[TreeNode]]:
        return list(split(root, target))
