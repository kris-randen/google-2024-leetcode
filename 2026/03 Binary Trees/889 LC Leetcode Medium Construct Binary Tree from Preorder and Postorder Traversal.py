"""

889. Construct Binary Tree from Preorder and Postorder Traversal
Medium

Given two integer arrays, preorder and postorder where preorder is the preorder traversal of a binary tree of distinct values and postorder is the postorder traversal of the same tree, reconstruct and return the binary tree.

If there exist multiple answers, you can return any of them.



Example 1:


Input: preorder = [1,2,4,5,3,6,7], postorder = [4,5,2,6,7,3,1]
Output: [1,2,3,4,5,6,7]
Example 2:

Input: preorder = [1], postorder = [1]
Output: [1]


Constraints:

1 <= preorder.length <= 30
1 <= preorder[i] <= preorder.length
All the values of preorder are unique.
postorder.length == preorder.length
1 <= postorder[i] <= postorder.length
All the values of postorder are unique.
It is guaranteed that preorder and postorder are the preorder traversal and postorder traversal of the same binary tree.

Seen this question in a real interview before?
1/6
Yes
No
Accepted
220,347/282.3K
Acceptance Rate
78.1%

"""
from typing import List, Optional


# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def tree_from_pp(preorder: List[int], postorder: List[int]):
    post_pos = {val: ind for ind, val in enumerate(postorder)}

    def size_left(pre_l, post_l):
        left_root = preorder[pre_l + 1]
        left_root_post_i = post_pos[left_root]
        return left_root_post_i - post_l + 1

    def build(
            pre_l,
            pre_r,
            post_l,
            post_r
    ):
        if pre_l >= pre_r:
            return None

        root = TreeNode(preorder[pre_l])

        if pre_r - pre_l == 1:
            return root

        size = size_left(pre_l, post_l)

        root.left = build(
            pre_l + 1,
            pre_l + 1 + size,
            post_l,
            post_l + size
        )

        root.right = build(
            pre_l + 1 + size,
            pre_r,
            post_l + size,
            post_r - 1
        )

        return root

    return build(0, len(preorder), 0, len(postorder))


class Solution:
    def constructFromPrePost(self, preorder: List[int], postorder: List[int]) -> Optional[TreeNode]:
        return tree_from_pp(preorder, postorder)



