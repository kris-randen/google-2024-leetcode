"""

107. Binary Tree Level Order Traversal II
Solved
Medium
Topics
Companies
Given the root of a binary tree, return the bottom-up level order traversal of its nodes' values. (i.e., from left to right, level by level from leaf to root).



Example 1:


Input: root = [3,9,20,null,null,15,7]
Output: [[15,7],[9,20],[3]]
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
684.8K
Submissions
1.1M

"""

# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

from collections import deque

def bfs(node):
    frontier = deque([[node]]); bfst = [[node.val]]
    while frontier:
        nds = frontier.popleft(); nxt = []
        for nd in nds:
            match nd:
                case TreeNode(left=lt, right=rt):
                    if lt: nxt.append(lt)
                    if rt: nxt.append(rt)
        if nxt:
            frontier.append(nxt)
            bfst.append([md.val for md in nxt])
    return bfst

def levelorderbottom(root):
    return bfs(root)[::-1]