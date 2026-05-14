"""

129. Sum Root to Leaf Numbers
Medium

You are given the root of a binary tree containing digits from 0 to 9 only.

Each root-to-leaf path in the tree represents a number.

For example, the root-to-leaf path 1 -> 2 -> 3 represents the number 123.
Return the total sum of all root-to-leaf numbers. Test cases are generated so that the answer will fit in a 32-bit integer.

A leaf node is a node with no children.



Example 1:


Input: root = [1,2,3]
Output: 25
Explanation:
The root-to-leaf path 1->2 represents the number 12.
The root-to-leaf path 1->3 represents the number 13.
Therefore, sum = 12 + 13 = 25.
Example 2:


Input: root = [4,9,0,5,1]
Output: 1026
Explanation:
The root-to-leaf path 4->9->5 represents the number 495.
The root-to-leaf path 4->9->1 represents the number 491.
The root-to-leaf path 4->0 represents the number 40.
Therefore, sum = 495 + 491 + 40 = 1026.


Constraints:

The number of nodes in the tree is in the range [1, 1000].
0 <= Node.val <= 9
The depth of the tree will not exceed 10.

Seen this question in a real interview before?
1/6
Yes
No
Accepted
1,281,169/1.8M
Acceptance Rate
69.9%

"""
from runpy import run_path
from typing import Optional, List


# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def is_leaf(node: Optional[TreeNode]) -> bool:
    return node is not None and node.left is None and node.right is None

def paths(root: Optional[TreeNode]) -> List[List[int]]:
    def dfs(node: Optional[TreeNode]):
        if node is None:
            return []

        if is_leaf(node):
            return [[node.val]]

        l_paths, r_paths = dfs(node.left), dfs(node.right)

        [path.append(node.val) for path in l_paths]
        [path.append(node.val) for path in r_paths]

        return l_paths + r_paths

    return [list(reversed(path)) for path in dfs(root)]

def path_to_num(ds):
    return int("".join(str(d) for d in ds))

def paths_number(root: Optional[TreeNode]) -> int:
    def dfs(node: Optional[TreeNode], number) -> int:
        if node is None:
            return 0

        number = 10 * number + node.val

        if is_leaf(node):
            return number

        return dfs(node.left, number) + dfs(node.right, number)

    return dfs(root, 0)

class Solution:
    def sumNumbers(self, root: Optional[TreeNode]) -> int:
        return paths_number(root)
