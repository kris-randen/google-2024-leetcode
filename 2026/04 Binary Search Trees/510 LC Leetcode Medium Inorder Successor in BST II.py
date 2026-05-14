"""

510. Inorder Successor in BST II
Medium
Topics
conpanies icon
Companies
Given a node in a binary search tree, return the in-order successor of that node in the BST. If that node has no in-order successor, return null.

The successor of a node is the node with the smallest key greater than node.val.

You will have direct access to the node but not to the root of the tree. Each node will have a reference to its parent node. Below is the definition for Node:

class Node {
    public int val;
    public Node left;
    public Node right;
    public Node parent;
}


Example 1:


Input: tree = [2,1,3], node = 1
Output: 2
Explanation: 1's in-order successor node is 2. Note that both the node and the return value is of Node type.
Example 2:


Input: tree = [5,3,6,2,4,null,null,1], node = 6
Output: null
Explanation: There is no in-order successor of the current node, so the answer is null.


Constraints:

The number of nodes in the tree is in the range [1, 104].
-105 <= Node.val <= 105
All Nodes will have unique values.


Follow up: Could you solve it without looking up any of the node's values?


Seen this question in a real interview before?
1/6
Yes
No
Accepted
76,097/124.6K
Acceptance Rate
61.1%

"""

from typing import Optional


# Definition for a Node.
class Node:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None
        self.parent = None

def is_right_child(node: Node):
    parent = node.parent
    return parent if (parent and parent.right is node) else None


def is_left_child(node: Node):
    parent = node.parent
    return parent if (parent and parent.left is node) else None

def leftmost(root: Node):
    if root.left is None:
        return root
    return leftmost(root.left)

def successor(node: Node) -> Optional[Node]:
    if node is None:
        return None

    if node.right:
        return leftmost(node.right)

    while parent := is_right_child(node):
        node = parent

    return node.parent if node.parent else None


class Solution:
    def inorderSuccessor(self, node: 'Node') -> 'Optional[Node]':
        return successor(node)
