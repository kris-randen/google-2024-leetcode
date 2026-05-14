"""

257. Binary Tree Paths
Easy

Given the root of a binary tree, return all root-to-leaf paths in any order.

A leaf is a node with no children.



Example 1:


Input: root = [1,2,3,null,5]
Output: ["1->2->5","1->3"]
Example 2:

Input: root = [1]
Output: ["1"]


Constraints:

The number of nodes in the tree is in the range [1, 100].
-100 <= Node.val <= 100

Seen this question in a real interview before?
1/6
Yes
No
Accepted
1,017,294/1.5M
Acceptance Rate
68.6%

"""

from typing import List, Optional

# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def is_leaf(node: Optional[TreeNode]) -> bool:
    return node is not None and node.left is None and node.right is None

def paths(root: Optional[TreeNode]) -> List[List[int]]:
    def dfs(node: Optional[TreeNode]) -> List[List[int]]:
        if node is None:
            return []

        if is_leaf(node):
            return [[node.val]]

        ps = dfs(node.left) + dfs(node.right)

        for path in ps:
            path.append(node.val)

        return ps

    return [list(reversed(path)) for path in dfs(root)]

def path_to_string(path: List[int]) -> str:
    return "->".join(str(p) for p in path)


class Solution:
    def binaryTreePaths(self, root: Optional[TreeNode]) -> List[str]:
        return [path_to_string(p) for p in paths(root)]
