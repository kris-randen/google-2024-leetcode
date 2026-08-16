"""

109. Convert Sorted List to Binary Search Tree
Solved
Medium
Topics
conpanies icon
Companies
Given the head of a singly linked list where elements are sorted in ascending order, convert it to a height-balanced binary search tree.



Example 1:


Input: head = [-10,-3,0,5,9]
Output: [0,-3,9,-10,null,5]
Explanation: One possible answer is [0,-3,9,-10,null,5], which represents the shown height balanced BST.
Example 2:

Input: head = []
Output: []


Constraints:

The number of nodes in head is in the range [0, 2 * 104].
-105 <= Node.val <= 105

Seen this question in a real interview before?
1/6
Yes
No
Accepted
696,018/1M
Acceptance Rate
66.6%

"""
from typing import Optional


# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def left_middle(a: Optional[ListNode]) -> Optional[ListNode]:
    if not a or not a.next:
        return a

    slow, fast = a, a.next.next
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next

    return slow


def split(a: Optional[ListNode]) -> tuple[Optional[ListNode], Optional[ListNode], Optional[ListNode]]:
    if not a or not a.next:
        return None, a, None

    mid = left_middle(a)
    root = mid.next
    mid.next = None
    right = root.next
    root.next = None
    return a, root, right


def list_to_tree(a: Optional[ListNode]) -> Optional[TreeNode]:
    if not a:
        return None

    return TreeNode(a.val)


def build(a: Optional[ListNode]) -> Optional[ListNode]:
    if not a or not a.next:
        return list_to_tree(a)

    left, root, right = split(a)
    root = list_to_tree(root)
    root.left = build(left)
    root.right = build(right)
    return root


class Solution:
    def sortedListToBST(self, head: Optional[ListNode]) -> Optional[TreeNode]:
        return build(head)
