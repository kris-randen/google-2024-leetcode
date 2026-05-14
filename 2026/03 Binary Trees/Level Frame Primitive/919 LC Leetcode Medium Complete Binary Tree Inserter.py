"""

919. Complete Binary Tree Inserter
Medium
Topics
conpanies icon
Companies
A complete binary tree is a binary tree in which every level, except possibly the last, is completely filled, and all nodes are as far left as possible.

Design an algorithm to insert a new node to a complete binary tree keeping it complete after the insertion.

Implement the CBTInserter class:

CBTInserter(TreeNode root) Initializes the data structure with the root of the complete binary tree.
int insert(int v) Inserts a TreeNode into the tree with value Node.val == val so that the tree remains complete, and returns the value of the parent of the inserted TreeNode.
TreeNode get_root() Returns the root node of the tree.


Example 1:


Input
["CBTInserter", "insert", "insert", "get_root"]
[[[1, 2]], [3], [4], []]
Output
[null, 1, 2, [1, 2, 3, 4]]

Explanation
CBTInserter cBTInserter = new CBTInserter([1, 2]);
cBTInserter.insert(3);  // return 1
cBTInserter.insert(4);  // return 2
cBTInserter.get_root(); // return [1, 2, 3, 4]


Constraints:

The number of nodes in the tree will be in the range [1, 1000].
0 <= Node.val <= 5000
root is a complete binary tree.
0 <= val <= 5000
At most 104 calls will be made to insert and get_root.

Seen this question in a real interview before?
1/6
Yes
No
Accepted
66,884/102.8K
Acceptance Rate
65.0%

"""
from collections import deque
from typing import Optional


# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def bfs_with_pos(root: Optional[TreeNode]):
    if root is None:
        return

    q = deque([(1, root)])

    while q:
        index, node = q.popleft()
        yield index, node

        if node.left:
            q.append((index * 2, node.left))
        if node.right:
            q.append((index * 2 + 1, node.right))


class CBTInserter:

    def __init__(self, root: Optional[TreeNode]):
        self.index_map = {}
        self.last = 0
        for index, node in bfs_with_pos(root):
            self.index_map[index] = node
            self.last = index

    def parent(self, index):
        return self.index_map[index // 2]

    def next_slot(self):
        self.last += 1
        return self.last, self.parent(self.last)

    @staticmethod
    def add_child(parent, child):
        if parent.left is None:
            parent.left = child
        else:
            parent.right = child

    def insert(self, val: int) -> int:
        index, parent = self.next_slot()
        child = TreeNode(val)

        self.add_child(parent, child)
        self.index_map[index] = child

        return parent.val


    def get_root(self) -> Optional[TreeNode]:
        return self.index_map[1]

# Your CBTInserter object will be instantiated and called as such:
# obj = CBTInserter(root)
# param_1 = obj.insert(val)
# param_2 = obj.get_root()