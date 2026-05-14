"""

116. Populating Next Right Pointers in Each Node
Solved
Medium

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
1/6
Yes
No
Accepted
1,338,352/2M
Acceptance Rate
67.1%

"""
from collections import deque
from typing import Optional, Iterator, List, Deque


# Definition for a Node.
class Node:
    def __init__(self, val: int = 0, left: 'Node' = None, right: 'Node' = None, next: 'Node' = None):
        self.val = val
        self.left = left
        self.right = right
        self.next = next

def level_nodes(root: Optional[Node]) -> Iterator[List[Node]]:
    if root is None:
        return

    q: Deque[Node] = deque([root])

    while q:
        level, level_size = [], len(q)

        for _ in range(level_size):
            node = q.popleft()
            level.append(node)

            if node.left:
                q.append(node.left)
            if node.right:
                q.append(node.right)

        yield level

def connect(level: List[Node]):
    prev = None

    for node in reversed(level):
        node.next = prev
        prev = node

def connect_all(levels: Iterator[List[Node]]):
    for level in levels:
        connect(level)


class Solution:
    def connect(self, root: 'Optional[Node]') -> 'Optional[Node]':
        connect_all(level_nodes(root))
        return root