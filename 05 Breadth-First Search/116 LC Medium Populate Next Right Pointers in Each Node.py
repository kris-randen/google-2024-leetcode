"""

116. Populating Next Right Pointers in Each Node
Solved
Medium
Topics
Companies
You are given a perfect binary tree where all leaves are on the same level, and every parent has two children. The binary tree has the following definition:

struct Node {
  int val;
  Node *left;
  Node *right;
  Node *next;
}
Populate each next pointer to point to its next right node. If there is no next right node, the next pointer should be set to NULL.

Initially, all next pointers are set to NULL.



Example 1:


Input: root = [1,2,3,4,5,6,7]
Output: [1,#,2,3,#,4,5,6,7,#]
Explanation: Given the above perfect binary tree (Figure A), your function should populate each next pointer to point to its next right node, just like in Figure B. The serialized output is in level order as connected by the next pointers, with '#' signifying the end of each level.
Example 2:

Input: root = []
Output: []


Constraints:

The number of nodes in the tree is in the range [0, 212 - 1].
-1000 <= Node.val <= 1000


Follow-up:

You may only use constant extra space.
The recursive approach is fine. You may assume implicit stack space does not count as extra space for this problem.
Seen this question in a real interview before?
1/5
Yes
No
Accepted
1.1M
Submissions
1.7M

"""
from typing import Optional


# Definition for a Node.
class Node:
    def __init__(self, val: int = 0, left: 'Node' = None, right: 'Node' = None, next: 'Node' = None):
        self.val = val
        self.left = left
        self.right = right
        self.next = next

from collections import deque

def bfs(node):
    frontier = deque([[node]]); bfst = [[node]]
    while frontier:
        nds = frontier.popleft(); nxt = []
        for nd in nds:
            match nd:
                case Node(left=lt, right=rt):
                    if lt: nxt.append(lt)
                    if rt: nxt.append(rt)
        if nxt:
            frontier.append(nxt)
            bfst.append(nxt)
    return bfst

def ct(nds):
    for i, nd in enumerate(nds):
        nd.next = nds[i + 1] if i + 1 < len(nds) else None

def cbfs(root):
    for bf in bfs(root): ct(bf)
    return root


# Constant Space Recursive Solution

def pct(rlts):
    for rlt in rlts:
        rlt[0].next = rlt[1]

def pcts(node):
    if not node.left and not node.right: return [node], [node]
    llt, lrt = pcts(node.left)
    rlt, rrt = pcts(node.right)
    pct(zip(lrt, rlt))
    rts = [node] + rrt
    lts = [node] + llt
    for rt in rts: rt.next = None
    return lts, rts

def bfsn(node):
    frontier = [[node]]
    for nds in frontier:
        nxt = [child for nd in nds for child in (nd.left, nd.right) if child]
        if nxt: frontier.append(nxt)
    return frontier

def cnds(nds):
    for i, nd in enumerate(nds):
        if i + 1 < len(nds): nd.next = nds[i + 1]
        else: nd.next = None

def cndss(ndss):
    for nds in ndss: cnds(nds)

def conn(node):
    cndss(bfsn(node)); return node

class Solution:
    def connect(self, root: 'Optional[Node]') -> 'Optional[Node]':
        if not root: return root
        return conn(root)