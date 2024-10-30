"""

117. Populating Next Right Pointers in Each Node II
Medium
Topics
Companies
Given a binary tree

struct Node {
  int val;
  Node *left;
  Node *right;
  Node *next;
}
Populate each next pointer to point to its next right node. If there is no next right node, the next pointer should be set to NULL.

Initially, all next pointers are set to NULL.



Example 1:


Input: root = [1,2,3,4,5,null,7]
Output: [1,#,2,3,#,4,5,7,#]
Explanation: Given the above binary tree (Figure A), your function should populate each next pointer to point to its next right node, just like in Figure B. The serialized output is in level order as connected by the next pointers, with '#' signifying the end of each level.
Example 2:

Input: root = []
Output: []


Constraints:

The number of nodes in the tree is in the range [0, 6000].
-100 <= Node.val <= 100


Follow-up:

You may only use constant extra space.
The recursive approach is fine. You may assume implicit stack space does not count as extra space for this problem.

"""

# Definition for a Node.
class Node:
    def __init__(self, val: int = 0, left: 'Node' = None, right: 'Node' = None, next: 'Node' = None):
        self.val = val
        self.left = left
        self.right = right
        self.next = next

from collections import deque

def bfs(node):
    frontier = [[node]]
    for nds in frontier:
        nxt = [
                child
                for nd in nds
                if nd
                for child in (nd.left, nd.right)
                if child
              ]
        if nxt: frontier.append(nxt)
    return frontier

def ct(nds):
    for i, nd in enumerate(nds):
        if nd: nd.next = nds[i + 1] if i + 1 < len(nds) else None

def cbfs(root):
    for bf in bfs(root): ct(bf)
    return root

class Solution:
    def connect(self, root: 'Node') -> 'Node':
        return cbfs(root)