"""

1676. Lowest Common Ancestor of a Binary Tree IV
Attempted
Medium

Given the root of a binary tree and an array of TreeNode objects nodes, return the lowest common ancestor (LCA) of all the nodes in nodes. All the nodes will exist in the tree, and all values of the tree's nodes are unique.

Extending the definition of LCA on Wikipedia: "The lowest common ancestor of n nodes p1, p2, ..., pn in a binary tree T is the lowest node that has every pi as a descendant (where we allow a node to be a descendant of itself) for every valid i". A descendant of a node x is a node y that is on the path from node x to some leaf node.



Example 1:


Input: root = [3,5,1,6,2,0,8,null,null,7,4], nodes = [4,7]
Output: 2
Explanation: The lowest common ancestor of nodes 4 and 7 is node 2.
Example 2:


Input: root = [3,5,1,6,2,0,8,null,null,7,4], nodes = [1]
Output: 1
Explanation: The lowest common ancestor of a single node is the node itself.

Example 3:


Input: root = [3,5,1,6,2,0,8,null,null,7,4], nodes = [7,6,2,4]
Output: 5
Explanation: The lowest common ancestor of the nodes 7, 6, 2, and 4 is node 5.


Constraints:

The number of nodes in the tree is in the range [1, 104].
-109 <= Node.val <= 109
All Node.val are unique.
All nodes[i] will exist in the tree.
All nodes[i] are distinct.

Seen this question in a real interview before?
1/6
Yes
No
Accepted
63,566/79.9K
Acceptance Rate
79.6%

"""

from typing import Optional, List

# Definition for a binary tree node.
class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


def lca_long(root: Optional[TreeNode], nodes: List[TreeNode]) -> Optional[TreeNode]:
    def dfs(node, nodes):
        n = len(nodes)
        flags = [False] * n

        if not node:
            return None, flags

        left_lca, left_flags = dfs(node.left, nodes)
        right_lca, right_flags = dfs(node.right, nodes)

        for i in range(n):
            flags[i] = left_flags[i] or right_flags[i] or node is nodes[i]

        if left_lca:
            return left_lca, flags

        if right_lca:
            return right_lca, flags

        if all(flags):
            return node, flags

        return None, flags

    lca_r, flags = dfs(root, nodes)
    return lca_r if all(flags) else None


def lca(root: TreeNode, nodes: List[TreeNode]) -> Optional[TreeNode]:
    targets = set(nodes)

    def dfs(node: Optional[TreeNode]):
        if not node:
            return None

        if node in targets:
            return node

        left = dfs(node.left)
        right = dfs(node.right)

        if left and right:
            return node

        return left or right

    return dfs(root)


class Solution:
    def lowestCommonAncestor(self, root: 'TreeNode', nodes: 'List[TreeNode]') -> 'TreeNode':
        return lca(root, nodes)
