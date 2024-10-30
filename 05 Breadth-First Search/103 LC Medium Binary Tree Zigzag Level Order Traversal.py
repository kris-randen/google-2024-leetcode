"""

103. Binary Tree Zigzag Level Order Traversal
Solved
Medium
Topics
Companies
Given the root of a binary tree, return the zigzag level order traversal of its nodes' values. (i.e., from left to right, then right to left for the next level and alternate between).



Example 1:


Input: root = [3,9,20,null,null,15,7]
Output: [[3],[20,9],[15,7]]
Example 2:

Input: root = [1]
Output: [[1]]
Example 3:

Input: root = []
Output: []


Constraints:

The number of nodes in the tree is in the range [0, 2000].
-100 <= Node.val <= 100
Seen this question in a real interview before?
1/5
Yes
No
Accepted
1.3M
Submissions
2.2M
Acceptance Rate
60.2%

"""

# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

from collections import deque

def bfsz(node):
    level = 1
    frontier = deque([[node]]); bfst = [[node.val]]
    while frontier:
        nds = frontier.popleft(); nxt = []
        for nd in reversed(nds):
            match nd:
                case TreeNode(left=lt, right=rt):
                    if level % 2 == 1:
                        if rt: nxt.append(rt)
                        if lt: nxt.append(lt)
                    else:
                        if lt: nxt.append(lt)
                        if rt: nxt.append(rt)
        if nxt:
            level += 1
            frontier.append(nxt)
            bfst.append([md.val for md in nxt])
    return bfst