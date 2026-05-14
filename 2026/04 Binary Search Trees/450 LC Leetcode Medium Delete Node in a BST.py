"""

450. Delete Node in a BST
Solved
Medium

Given a root node reference of a BST and a key, delete the node with the given key in the BST. Return the root node reference (possibly updated) of the BST.

Basically, the deletion can be divided into two stages:

Search for a node to remove.
If the node is found, delete the node.


Example 1:


Input: root = [5,3,6,2,4,null,7], key = 3
Output: [5,4,6,2,null,null,7]
Explanation: Given key to delete is 3. So we find the node with value 3 and delete it.
One valid answer is [5,4,6,2,null,null,7], shown in the above BST.
Please notice that another valid answer is [5,2,6,null,4,null,7] and it's also accepted.

Example 2:

Input: root = [5,3,6,2,4,null,7], key = 0
Output: [5,3,6,2,4,null,7]
Explanation: The tree does not contain a node with value = 0.
Example 3:

Input: root = [], key = 0
Output: []


Constraints:

The number of nodes in the tree is in the range [0, 104].
-105 <= Node.val <= 105
Each node has a unique value.
root is a valid binary search tree.
-105 <= key <= 105


Follow up: Could you solve it with time complexity O(height of tree)?


Seen this question in a real interview before?
1/6
Yes
No
Accepted
869,425/1.6M
Acceptance Rate
54.6%

"""


from typing import Optional


# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def leftmost(root: TreeNode):
    while root.left:
        root = root.left
    return root


def rightmost(root: TreeNode):
    while root.right:
        root = root.right
    return root


def delete_min(node: TreeNode):
    if node.left is None:
        return None

    node.left = delete_min(node.left)
    return node


def delete(root: Optional[TreeNode], key: int):
    if root is None:
        return None

    if key < root.val:
        root.left = delete(root.left, key)
        return root

    if key > root.val:
        root.right = delete(root.right, key)
        return root

    if root.left is None:
        return root.right

    if root.right is None:
        return root.left

    nxt = leftmost(root.right)
    nxt.right = delete_min(root.right)
    nxt.left = root.left

    return nxt


class Solution:
    def deleteNode(self, root: Optional[TreeNode], key: int) -> Optional[TreeNode]:
        return delete(root, key)

