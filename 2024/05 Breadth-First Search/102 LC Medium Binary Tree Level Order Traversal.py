"""

102. Binary Tree Level Order Traversal
Solved
Medium
Topics
Companies
Given the root of a binary tree, return the level order traversal of its nodes' values. (i.e., from left to right, level by level).

Example 1:

Input: root = [3,9,20,null,null,15,7]
Output: [[3],[9,20],[15,7]]
Example 2:

Input: root = [1]
Output: [[1]]
Example 3:

Input: root = []
Output: []


Constraints:

The number of nodes in the tree is in the range [0, 2000].
-1000 <= Node.val <= 1000
Seen this question in a real interview before?
1/5
Yes
No
Accepted
2.5M
Submissions
3.6M
Acceptance Rate
68.8%

"""

# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

from collections import deque
from functools import reduce


def bfs(node):
    frontier, bfst = deque([[node]]), [[node.val]]
    while frontier:
        nxt = []; nds = frontier.popleft()
        for nd in nds:
            match nd:
                case TreeNode(left=lt, right=rt):
                    if lt: nxt.append(lt)
                    if rt: nxt.append(rt)
        if not nxt: continue
        bfst.append([md.val for md in nxt])
        frontier.append(nxt)
    return bfst

def bfs_reduce(node):
    def agg(acc, nd):
        return (
                acc +
                [nd.left] * (nd.left is not None) +
                [nd.right] * (nd.right is not None)
               )

    for nds in (frontier := [[node]]):
        nxt = reduce(agg,nds,[])
        if nxt: frontier.append(nxt)

    return [[nd.val for nd in nds] for nds in frontier]

def bfs_gen(node):
    for nds in (frontier := [[node]]):
        nxt = [child for nd in nds for child in (nd.left, nd.right) if child]
        if nxt: frontier.append(nxt)
    return [[nd.val for nd in nds] for nds in frontier]




