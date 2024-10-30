"""

199. Binary Tree Right Side View
Solved
Medium
Topics
Companies
Given the root of a binary tree, imagine yourself standing on the right side of it, return the values of the nodes you can see ordered from top to bottom.

Example 1:

Input: root = [1,2,3,null,5,null,4]
Output: [1,3,4]
Example 2:

Input: root = [1,null,3]
Output: [1,3]
Example 3:

Input: root = []
Output: []

Constraints:

The number of nodes in the tree is in the range [0, 100].
-100 <= Node.val <= 100
Seen this question in a real interview before?
1/5
Yes
No
Accepted
1.5M
Submissions
2.4M
Acceptance Rate
64.1%

"""

from typing import Optional, List

# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def rsv(node):
    match node:
        case TreeNode(left=lt, right=rt):
            lrsv, rrsv = rsv(lt), rsv(rt)
            return [node] + rrsv + (lrsv[len(rrsv):])
        case None: return []

class Solution:
    def rightSideView(self, root: Optional[TreeNode]) -> List[int]:
        if not root: return []
        return [nd.val for nd in rsv(root)]





